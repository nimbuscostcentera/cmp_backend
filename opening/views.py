from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
import json
from .models import (
    OpeningVendorRawMaterial,
    OpeningRawMaterial,
    VendorStoneOpening,
    SelfStoneOpening,
    OpeningDesignStock,
    OpeningDesignStockStone,
    OpeningDesignStockColor,
)
from .serializers import (
    OpeningVendorRawMaterialSerializer,
    OpeningRawMaterialSerializer,
    VendorStoneOpeningSerializer,
    SelfStoneOpeningSerializer,
    OpeningDesignStockSerializer,
    OpeningDesignStockStoneSerializer,
    OpeningDesignStockColorSerializer,
)


class OpeningList(APIView):
    """
    Dynamic handler for all Opening types
    - Raw Material (Vendor/Self)
    - Stone (Vendor/Self)
    - Design Stock (Header/Stone/Color)
    """

    TYPE_MAP = {
        # Layout A
        "vendor_raw": (OpeningVendorRawMaterial, OpeningVendorRawMaterialSerializer),
        "self_raw": (OpeningRawMaterial, OpeningRawMaterialSerializer),
        # Layout B
        "vendor_stone": (VendorStoneOpening, VendorStoneOpeningSerializer),
        "self_stone": (SelfStoneOpening, SelfStoneOpeningSerializer),
        # Layout C
        "design_header": (OpeningDesignStock, OpeningDesignStockSerializer),
        "design_stone": (OpeningDesignStockStone, OpeningDesignStockStoneSerializer),
        "design_color": (OpeningDesignStockColor, OpeningDesignStockColorSerializer),
    }

    def get_model_and_serializer(self, mtype):
        return self.TYPE_MAP.get(mtype, (None, None))

    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        if not mtype:
            return Response({"message": "type parameter required"}, status=status.HTTP_400_BAD_REQUEST)
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        if pk:
            instance = get_object_or_404(model, pk=pk)
            return Response(serializer(instance).data)

        # Handle child models (stone/color)
        if mtype in ["design_stone", "design_color"]:
            header_id = request.query_params.get("Header")
            if not header_id:
                return Response({"message": "Header is required"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = model.objects.filter(Header_id=header_id)
        else:
            queryset = model.objects.all()

        return Response(serializer(queryset, many=True).data)

    @transaction.atomic
    def post(self, request):
        mtype = request.data.get("type")
        if not mtype:
            return Response({"message": "type is required"}, status=status.HTTP_400_BAD_REQUEST)

        model, serializer_class = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        # ----------------------------
        # CASE 1: DESIGN HEADER CREATION
        # ----------------------------
        if mtype == "design_header":
            data = request.data.copy()
            stones = data.pop("stones", [])
            colors = data.pop("colors", [])

            serializer = serializer_class(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            header_instance = serializer.save()

            # Save stones if provided
            if stones:
                for stone in stones:
                    stone["Header"] = header_instance.ID
                stone_serializer = OpeningDesignStockStoneSerializer(data=stones, many=True)
                if not stone_serializer.is_valid():
                    transaction.set_rollback(True)
                    return Response(stone_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                stone_serializer.save()

            # Save colors if provided
            if colors:
                for color in colors:
                    color["Header"] = header_instance.ID
                color_serializer = OpeningDesignStockColorSerializer(data=colors, many=True)
                if not color_serializer.is_valid():
                    transaction.set_rollback(True)
                    return Response(color_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                color_serializer.save()

            return Response(
                {"message": "Design header created successfully", "ID": header_instance.ID},
                status=status.HTTP_201_CREATED,
            )

        # ----------------------------
        # CASE 2: DESIGN STONE / COLOR CREATION
        # ----------------------------
        elif mtype in ["design_stone", "design_color"]:
            header_id = request.data.get("Header")
            if not header_id:
                return Response({"message": "Header is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify header exists
            header_instance = OpeningDesignStock.objects.filter(pk=header_id).first()
            if not header_instance:
                return Response(
                    {"message": f"Design header with ID {header_id} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            raw_data = request.data.get("data", [])
            if isinstance(raw_data, str):
                try:
                    raw_data = json.loads(raw_data)
                except json.JSONDecodeError:
                    raw_data = []

            if not isinstance(raw_data, list):
                raw_data = [raw_data]

            # Attach header ID to all rows
            for row in raw_data:
                row["Header"] = header_id

            serializer = serializer_class(data=raw_data, many=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            created_instances = serializer.save()

            # ----------------------------
            # ✅ Update parent ColorS only when adding design_color
            # ----------------------------
            if mtype == "design_color":
                new_color_ids = [str(item.Color_id) for item in created_instances if hasattr(item, "Color_id")]
                existing_colors = [c for c in header_instance.ColorS.split(",") if c.strip()] if header_instance.ColorS else []
                
                # Append unique new colors
                updated_colors = list(dict.fromkeys(existing_colors + new_color_ids))
                header_instance.ColorS = ",".join(updated_colors)
                header_instance.save()

            return Response(
                {"message": f"{mtype.replace('design_', '').capitalize()} added successfully"},
                status=status.HTTP_201_CREATED,
            )

        # ----------------------------
        # CASE 3: OTHER TYPES (RAW/STONE SELF/VENDOR)
        # ----------------------------
        else:
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": f"{mtype} created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer_class = self.get_model_and_serializer(mtype)
        
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        instance = get_object_or_404(model, pk=pk)
        serializer = serializer_class(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # Update subtable first

            # -----------------------------
            # If updating design_color, update parent header ColorS from request
            # -----------------------------
            if mtype == "design_color" and "ColorS" in request.data:
                header_id = instance.Header_id  # FK to parent header
                header_instance = OpeningDesignStock.objects.get(pk=header_id)
                header_instance.ColorS = request.data["ColorS"]  # directly use payload
                header_instance.save()

            return Response({"message": f"{mtype} updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)

        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        instance = get_object_or_404(model, pk=pk)

        # -----------------------------
        # If deleting a design_color row, update parent header's ColorS
        # -----------------------------
        if mtype == "design_color":
            header_id = instance.Header_id  # FK reference to OpeningDesignStock
            from .models import OpeningDesignStock  # avoid circular imports

            header_instance = OpeningDesignStock.objects.filter(pk=header_id).first()

            if header_instance and header_instance.ColorS:
                # Convert the ColorS field ("3,2,7") into a list
                color_ids = [c for c in header_instance.ColorS.split(",") if c.strip()]

                # Get the color ID from the record being deleted
                color_to_remove = str(instance.Color_id)  # ✅ corrected

                # Remove it from the list if present
                if color_to_remove in color_ids:
                    color_ids.remove(color_to_remove)

                # Save the updated ColorS string
                header_instance.ColorS = ",".join(color_ids)
                header_instance.save()

        # -----------------------------
        # Delete the actual record
        # -----------------------------
        instance.delete()
        return Response({"message": f"{mtype} deleted successfully"}, status=status.HTTP_200_OK)



