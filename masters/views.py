import json
from urllib import request
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal
from .models import (
    CompanyMaster, DesignItemType, ItemTypeMaster, StoneRateSetting, StoneRateSettingMiscCharge, YearMaster, UserMaster, UnitMaster, SizeMaster,
    StoneMaster, StoneSubMaster, ColorMaster, PlatingMaster,
    MiscChargeMaster, PlatingPolishMaster, ItemMaster, DesignGroupMaster,
    SystemMaster, RawMaterialMaster, ProcessMaster, DepartmentMaster, StaffMaster, ArtisanMaster,
    DealerMaster, CustomerMaster, DesignMaster, DesignDetail
)

from .serializers import (
    CompanyMasterSerializer,
    DesignItemTypeDetailSerializer,
    ItemTypeMasterSerializer,
    StoneRateSettingMiscChargeSerializer,
    StoneRateSettingSerializer,
    UnitMasterSerializer, SizeMasterSerializer, StoneMasterSerializer,
    StoneSubMasterSerializer, ColorMasterSerializer, PlatingMasterSerializer,
    MiscChargeMasterSerializer, PlatingPolishMasterSerializer,
    ItemMasterSerializer, DesignGroupMasterSerializer, SystemMasterSerializer,
    RawMaterialMasterSerializer, DesignMasterSerializer, 
    ProcessMasterSerializer, DepartmentMasterSerializer, StaffMasterSerializer,
    ArtisanMasterSerializer, DealerMasterSerializer, CustomerMasterSerializer, DesignMasterSerializer, DesignDetailSerializer
)


# -------------------------------
# Generic CRUD Mixin
# -------------------------------
class MasterMixin:
    TYPE_MAP = {}

    def get_model_and_serializer(self, mtype):
        return self.TYPE_MAP.get(mtype, (None, None))

    def list_or_detail(self, model, serializer_class, pk):
        if pk:
            try:
                instance = model.objects.get(pk=pk)
            except model.DoesNotExist:
                return Response({"message": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializer_class(instance)
            return Response(serializer.data)
        qs = model.objects.all()
        serializer = serializer_class(qs, many=True)
        return Response(serializer.data)

    def create(self, serializer_class, data):
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, model, serializer_class, pk, data):
        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({"message": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializer_class(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, model, pk):
        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({"message": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# -------------------------------
# Root / Hello
# -------------------------------
def home_view(request):
    return HttpResponse("Welcome to the Home Page")


class HelloAPI(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})


# -------------------------------
# Layout APIs
# -------------------------------
class Layout1List(APIView, MasterMixin):
    """
    Handles: ColorMaster, MiscChargeMaster, DesignGroupMaster, ItemMaster, SizeMaster, PlatingMaster, ItemTypeMaster
    """
    TYPE_MAP = {
        "cm": (ColorMaster, ColorMasterSerializer),
        "mm": (MiscChargeMaster, MiscChargeMasterSerializer),
        "dgm": (DesignGroupMaster, DesignGroupMasterSerializer),
        "im": (ItemMaster, ItemMasterSerializer),
        "szm": (SizeMaster, SizeMasterSerializer),
        "pm": (PlatingMaster, PlatingMasterSerializer),
        "itm": (ItemTypeMaster, ItemTypeMasterSerializer),
    }

    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout2List(APIView, MasterMixin):
    """
    Handles: DepartmentMaster, StoneMaster
    """
    TYPE_MAP = {
        "dm": (DepartmentMaster, DepartmentMasterSerializer),
        "sm": (StoneMaster, StoneMasterSerializer),
    }
    # Same methods as Layout1
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout3List(APIView, MasterMixin):
    """
    Handles: ArtisanMaster, DealerMaster
    """
    TYPE_MAP = {
        "am": (ArtisanMaster, ArtisanMasterSerializer),
        "dmr": (DealerMaster, DealerMasterSerializer),
    }
    # Methods same pattern as above
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout4List(APIView, MasterMixin):
    TYPE_MAP = {
        "stf": (StaffMaster, StaffMasterSerializer),
    }
    # Methods same pattern as above...
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout5List(APIView, MasterMixin):
    TYPE_MAP = {
        "cust": (CustomerMaster, CustomerMasterSerializer),
    }
    # Methods same pattern as above...
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout6List(APIView, MasterMixin):
    TYPE_MAP = {
        "rmm": (RawMaterialMaster, RawMaterialMasterSerializer),
    }
    # Methods same pattern as above...
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout7List(APIView, MasterMixin):
    TYPE_MAP = {
        "prm": (ProcessMaster, ProcessMasterSerializer),
    }
    # Methods same pattern as above...
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout8List(APIView, MasterMixin):
    TYPE_MAP = {
        "ppm": (PlatingPolishMaster, PlatingPolishMasterSerializer),
    }
    # Methods same pattern as above...
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)


class Layout10List(APIView, MasterMixin):
    TYPE_MAP = {
        "ssm": (StoneSubMaster, StoneSubMasterSerializer),
    }
    # Methods same pattern as above...
    def get(self, request, pk=None):
        mtype = request.query_params.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.list_or_detail(model, serializer, pk)

    def post(self, request):
        mtype = request.data.get("type")
        _, serializer = self.get_model_and_serializer(mtype)
        if not serializer:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(serializer, request.data)

    def put(self, request, pk):
        mtype = request.data.get("type")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(model, serializer, pk, request.data)

    def delete(self, request, pk):
        mtype = request.query_params.get("type")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(model, pk)




class SpcpmasterList(APIView, MasterMixin):
    TYPE_MAP = {
        "header": (StoneRateSetting, StoneRateSettingSerializer),
        "detail": (StoneRateSettingMiscCharge, StoneRateSettingMiscChargeSerializer),
    }

    def get(self, request, pk=None):
        mtype = request.query_params.get("type", "header")
        model, serializer = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        # Special case for fetching details by header id
        if mtype == "detail" and not pk:
            header_id = request.query_params.get("ID_Header")
            if not header_id:
                return Response({"message": "ID_Header is required for detail fetch"},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = model.objects.filter(ID_Header_id=header_id)
            return Response(serializer(queryset, many=True).data)

        return self.list_or_detail(model, serializer, pk)

    @transaction.atomic
    def post(self, request):
        mtype = request.data.get("type", "header")

        if mtype == "header":
            serializer = StoneRateSettingSerializer(data=request.data)
            if serializer.is_valid():
                header = serializer.save()
                return Response(
                    {"message": "Created successfully", "header_id": header.ID},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif mtype == "detail":
            details_data = request.data

        # Ensure details_data is a dict
        if isinstance(details_data, str):
            import json
            details_data = json.loads(details_data)

        # Extract header ID
        header_id = details_data.get("ID_Header")
        if not header_id:
            return Response({"message": "ID_Header is required for adding details"},
                            status=status.HTTP_400_BAD_REQUEST)

        header = get_object_or_404(StoneRateSetting, ID=header_id)

        # Get detail rows as list
        rows = []
        for key, val in details_data.items():
            if key.isdigit():  # Only numeric keys are detail rows
                rows.append(val)

        

        new_amount_sum = Decimal('0.0')

        for detail in rows:
            detail.pop("rowid", None)
            detail.pop("ID_Header", None)

            misc_charge_instance = get_object_or_404(MiscChargeMaster, ID=detail["ID_MiscCharge"])

            StoneRateSettingMiscCharge.objects.create(
                ID_Header=header,
                ID_MiscCharge=misc_charge_instance,
                Amount=Decimal(detail.get("Amount", "0.0")),
            )

            new_amount_sum += Decimal(detail.get("Amount", "0.0"))

        # Update SP
        header.SP = (header.SP or Decimal('0.0')) + new_amount_sum
        header.save()

        return Response(
            {"message": "Details added and SP updated successfully", "added_amount": new_amount_sum},
            status=status.HTTP_201_CREATED
        )


# kindly correct the indentation of the following code
    @transaction.atomic
    def put(self, request, pk):

        mtype = request.data.get("type")
        if not mtype:
            return Response({"message": "Type is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Get model & serializer
        model, serializer_class = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        if mtype == "header":
            # Update header fields
            serializer = serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Header updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif mtype == "detail":
            # Update the detail row
            detail_fields = {}
            if "ID_MiscCharge" in request.data:
                detail_fields["ID_MiscCharge"] = request.data["ID_MiscCharge"]
            if "Amount" in request.data:
                detail_fields["Amount"] = request.data["Amount"]

            StoneRateSettingMiscCharge.objects.filter(ID=pk).update(**detail_fields)

            # Update SP in header if provided
            recalculated_sp = request.data.get("SP")
            if recalculated_sp is not None:
                header_instance = instance.ID_Header
                header_instance.SP = recalculated_sp
                header_instance.save()

            return Response({"message": "Detail updated successfully"}, status=status.HTTP_200_OK)


# kindly correct the indentation of the following code
    @transaction.atomic
    def delete(self, request, pk):
        """
        Delete header or detail.
        For detail deletion, recalculate the header SP.
        """
        mtype = request.query_params.get("type", "header")
        model, _ = self.get_model_and_serializer(mtype)
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        if mtype == "header":
            # Delete header and all related details
            instance.delete()
            return Response({"message": "Header deleted successfully"}, status=status.HTTP_200_OK)

        elif mtype == "detail":
            # Keep reference to header
            header_instance = instance.ID_Header

            # Delete the detail row
            instance.delete()

            # Recalculate SP for the header
            total_cp = header_instance.CP or 0
            from django.db.models import Sum
            total_misc = (
                StoneRateSettingMiscCharge.objects.filter(ID_Header=header_instance)
                .aggregate(total_amount=Sum("Amount"))["total_amount"]
                or 0
            )
            header_instance.SP = float(total_cp) + float(total_misc)
            header_instance.save()

            return Response(
                {"message": "Detail deleted successfully, SP recalculated"},
                status=status.HTTP_200_OK,
            )
            




class Layout9List(APIView, MasterMixin):
    TYPE_MAP = {
        "header": (DesignMaster, DesignMasterSerializer),
        "detail": (DesignDetail, DesignDetailSerializer),
        "itemtype": (DesignItemType, DesignItemTypeDetailSerializer),
    }

    def get_model_and_serializer(self, mtype):
        return self.TYPE_MAP.get(mtype, (None, None))

    def get(self, request, pk=None):
        mtype = request.query_params.get("type", "header")
        model, serializer = self.get_model_and_serializer(mtype)

        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch DesignDetail by header ID
        if mtype == "detail" and not pk:
            header_id = request.query_params.get("ID_Header")
            if not header_id:
                return Response({"message": "ID_Header is required for detail fetch"},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = model.objects.filter(ID_Header=header_id)
            return Response(serializer(queryset, many=True).data)

        # Fetch DesignItemType by header ID
        if mtype == "itemtype" and not pk:
            header_id = request.query_params.get("ID_Header")
            if not header_id:
                return Response({"message": "ID_Header is required for itemtype fetch"},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = model.objects.filter(ID_Header_id=header_id)
            return Response(serializer(queryset, many=True).data)

        # Default: fetch list or detail by pk
        return self.list_or_detail(model, serializer, pk)

    @transaction.atomic
    def post(self, request):
        mtype = request.data.get("type", "header")
        model, serializer_class = self.get_model_and_serializer(mtype)

        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        # 🧠 CASE 1: HEADER CREATION
        if mtype == "header":
            data = request.data.copy()

            # parse Details and ItemTypeDetails if present
            details = data.get("Details")
            itemtype = data.get("ItemTypeDetails")

            if details:
                try:
                    if isinstance(details, str):
                        details = json.loads(details)
                except json.JSONDecodeError:
                    details = []
            else:
                details = []

            if itemtype:
                try:
                    if isinstance(itemtype, str):
                        itemtype = json.loads(itemtype)
                except json.JSONDecodeError:
                    itemtype = []
            else:
                itemtype = []

            serializer = serializer_class(data=data)
            if serializer.is_valid():
                validated = serializer.validated_data
                validated["Details"] = details
                validated["ItemTypeDetails"] = itemtype
                header = serializer.create(validated)
                return Response(
                    {"message": "Header created successfully", "DesignID": header.DesignID},
                    status=status.HTTP_201_CREATED,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 🧠 CASE 2: DETAIL OR ITEMTYPE CREATION
        elif mtype in ["detail", "itemtype"]:
            ID_Header = request.data.get("ID_Header")
            if not ID_Header:
                return Response(
                    {"message": "ID_Header is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                header = get_object_or_404(DesignMaster, DesignID=ID_Header)
                print(f"Header instance found: {header}")
            except DesignMaster.DoesNotExist:
                return Response(
                    {"message": f"DesignMaster with ID {ID_Header} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            raw_data = request.data.get("data", [])
            print(f"Raw data received: {raw_data}")
            if isinstance(raw_data, str):
                try:
                    raw_data = json.loads(raw_data)
                except json.JSONDecodeError:
                    raw_data = []

            serializer = serializer_class(data=raw_data, many=True)
            if serializer.is_valid():
                serializer.save(ID_Header=header)  # ✅ Correct way
                return Response(
                    {"message": f"{mtype.capitalize()} records added successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



 
    @transaction.atomic
    def put(self, request, pk):
        data = request.data.copy()
        files = request.FILES
        mtype = data.get("type", "header")
        model, serializer_class = self.get_model_and_serializer(mtype)
 
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
 
        serializer = serializer_class(instance, data=data, partial=True)
 
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{mtype.capitalize()} updated successfully"}, status=status.HTTP_200_OK)
 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    @transaction.atomic
    def delete(self, request, pk):
        mtype = request.query_params.get("type", "header")
        model, _ = self.get_model_and_serializer(mtype)
 
        if not model:
            return Response({"message": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
 
        instance.delete()
        msg = "Header deleted successfully" if mtype == "header" else "Detail deleted successfully"
        return Response({"message": msg}, status=status.HTTP_200_OK)




# UNITMASTER-> LIST AND DETAIL:
class UnitMasterList(APIView):
    """
    GET: List all colors
    POST: Create a new color
    """
    def get(self, request):
        units = UnitMaster.objects.all()
        serializer = UnitMasterSerializer(units, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UnitMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UnitMasterDetail(APIView):
    """
    GET: Retrieve a single color
    PUT: Update a color
    DELETE: Delete a color
    """
    def get_object(self, pk):
        try:
            return UnitMaster.objects.get(pk=pk)
        except UnitMaster.DoesNotExist:
            return None

    def get(self, request, pk):
        unit = self.get_object(pk)
        if not unit:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UnitMasterSerializer(unit)
        return Response(serializer.data)

    def put(self, request, pk):
        unit = self.get_object(pk)
        if not unit:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UnitMasterSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        unit = self.get_object(pk)
        if not unit:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)