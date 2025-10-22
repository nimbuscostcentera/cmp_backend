# serializers.py
from rest_framework import serializers
from django.db import IntegrityError, transaction
from .models import (
    OpeningVendorRawMaterial,
    OpeningRawMaterial,
    VendorStoneOpening,
    SelfStoneOpening,
    OpeningDesignStock,
    OpeningDesignStockStone,
    OpeningDesignStockColor
)
from masters.models import ColorMaster, StoneSubMaster

from masters.models import (
    DepartmentMaster,
    DesignMaster,
    ItemTypeMaster,
    ItemMaster,
    SizeMaster,
    StoneMaster,
    StoneSubMaster,
    ColorMaster
)
# -------------------------------
# TAB 1: Vendor Raw Material
# -------------------------------
class OpeningVendorRawMaterialSerializer(serializers.ModelSerializer):
    VendorGroup_Name = serializers.CharField(source="VendorGroup.VendorGrp_Name", read_only=True)
    Vendor_Name = serializers.CharField(source="Vendor.Vendor_Name", read_only=True)
    RawMaterial_Name = serializers.CharField(source="RawMaterial.Raw_Code", read_only=True)

    class Meta:
        model = OpeningVendorRawMaterial
        fields = "__all__"
        read_only_fields = ("ID", "Srl")

    def validate(self, data):
        required = ("VendorGroup", "Vendor", "RawMaterial", "Qty", "DrCr")
        if any(field in data for field in required):
            missing = [f for f in required if f not in data or data.get(f) in (None, "")]
            if missing:
                raise serializers.ValidationError({f: "This field is required." for f in missing})
        return data

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"non_field_errors": ["Duplicate Vendor + RawMaterial combination not allowed."]}
            )


# -------------------------------
# TAB 2: Self Raw Material
# -------------------------------
class OpeningRawMaterialSerializer(serializers.ModelSerializer):
    Department_Name = serializers.CharField(source="Department.Code", read_only=True)
    RawMaterial_Name = serializers.CharField(source="RawMaterial.Raw_Code", read_only=True)

    class Meta:
        model = OpeningRawMaterial
        fields = "__all__"
        read_only_fields = ("ID", "Srl")

    def validate(self, data):
        required = ("Department", "RawMaterial", "Qty", "DrCr")
        if any(field in data for field in required):
            missing = [f for f in required if f not in data or data.get(f) in (None, "")]
            if missing:
                raise serializers.ValidationError({f: "This field is required." for f in missing})
        return data

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"non_field_errors": ["Duplicate Department + RawMaterial combination not allowed."]}
            )


# -------------------------------
# TAB 3A: Vendor Stone Opening
# -------------------------------
class VendorStoneOpeningSerializer(serializers.ModelSerializer):
    VendorGroup_Name = serializers.CharField(source="VendorGroup.VendorGrp_Name", read_only=True)
    Vendor_Name = serializers.CharField(source="Vendor.Vendor_Name", read_only=True)
    StoneMain_Name = serializers.CharField(source="StoneMain.Code", read_only=True)
    StoneSub_Name = serializers.CharField(source="StoneSub.Sub_Code", read_only=True)
    Color_Name = serializers.CharField(source="Color.Code", read_only=True)

    class Meta:
        model = VendorStoneOpening
        fields = "__all__"
        read_only_fields = ("ID", "Srl")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"non_field_errors": ["Duplicate Vendor + StoneMain + StoneSub + Color not allowed."]}
            )


# -------------------------------
# TAB 3: Self Stone Opening
# -------------------------------
class SelfStoneOpeningSerializer(serializers.ModelSerializer):
    Department_Name = serializers.CharField(source="Department.Code", read_only=True)
    StoneMain_Name = serializers.CharField(source="StoneMain.Code", read_only=True)
    StoneSub_Name = serializers.CharField(source="StoneSub.Sub_Code", read_only=True)
    Color_Name = serializers.CharField(source="Color.Code", read_only=True)

    class Meta:
        model = SelfStoneOpening
        fields = "__all__"
        read_only_fields = ("ID", "Srl")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"non_field_errors": ["Duplicate Department + StoneMain + StoneSub + Color not allowed."]}
            )


# -------------------------------
# TAB 4: Design Opening (Header + Stone + Color)
# -------------------------------
class OpeningDesignStockStoneSerializer(serializers.ModelSerializer):
    StoneM_name = serializers.CharField(source="ID_StoneM.Code", read_only=True)
    Color_name = serializers.CharField(source="ID_Color.Code", read_only=True)
    StoneS_name = serializers.CharField(source="ID_StoneS.Sub_Code", read_only=True)
    class Meta:
        model = OpeningDesignStockStone
        fields = '__all__'


class OpeningDesignStockColorSerializer(serializers.ModelSerializer):
    Color_name = serializers.CharField(source="Color.Code", read_only=True)
    class Meta:
        model = OpeningDesignStockColor
        fields = '__all__'


class OpeningDesignStockSerializer(serializers.ModelSerializer):

    ID_Department_Code = serializers.CharField(source="ID_Department.Code", read_only=True)
    ID_Design_Code = serializers.CharField(source="ID_Design.Design_Code", read_only=True)
    ID_ItemType_Code = serializers.CharField(source="ID_ItemType.Code", read_only=True)
    ID_Item_Code = serializers.CharField(source="ID_Item.Code", read_only=True)
    ID_Size_Code = serializers.CharField(source="ID_Size.Code", read_only=True)

    class Meta:
        model = OpeningDesignStock
        fields = '__all__'
        read_only_fields = ('Srl', 'ID', 'Trancode')

