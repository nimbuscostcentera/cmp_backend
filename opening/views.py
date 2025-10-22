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
        # DESIGN HEADER: with nested stones/colors
        # ----------------------------
        if mtype == "design_header":
            data = request.data.copy()

            # Extract nested stones and colors safely
            stones = data.pop("stones", [])
            colors = data.pop("colors", [])

            serializer = serializer_class(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            instance = serializer.save()  # Create Header first

            # Validate and save stones
            if stones:
                # Validate required fields rule:
                for stone in stones:
                    if stone.get("ID_StoneM") and stone.get("ID_StoneS"):
                        missing = [
                            key for key in ["Pcs", "Weight", "ID_Color"]
                            if not stone.get(key)
                        ]
                        if missing:
                            return Response(
                                {"error": f"Missing mandatory fields {missing} when both ID_StoneM and ID_StoneS exist"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                    # Set foreign key Header
                    stone["Header"] = instance.ID

                stone_serializer = OpeningDesignStockStoneSerializer(data=stones, many=True)
                if stone_serializer.is_valid():
                    stone_serializer.save()
                else:
                    # Rollback header if stones invalid
                    transaction.set_rollback(True)
                    return Response(stone_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Validate and save colors
            if colors:
                for color in colors:
                    color["Header"] = instance.ID

                color_serializer = OpeningDesignStockColorSerializer(data=colors, many=True)
                if color_serializer.is_valid():
                    color_serializer.save()
                else:
                    transaction.set_rollback(True)
                    return Response(color_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"message": "Header, Stones, and Colors created successfully", "ID": instance.ID},
                status=status.HTTP_201_CREATED,
            )

        # ----------------------------
        # Other (simple) types
        # ----------------------------
        serializer = serializer_class(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{mtype} record(s) added successfully"}, status=status.HTTP_201_CREATED)
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
            serializer.save()
            return Response({"message": f"{mtype} updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(model, pk=pk)
        instance.delete()
        return Response({"message": f"{mtype} deleted successfully"}, status=status.HTTP_200_OK)
