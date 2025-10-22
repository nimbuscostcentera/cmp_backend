from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    ColorMaster, DesignDetail, ItemTypeMaster, MappingTC, SizeMaster, StoneRateSetting, StoneRateSettingMiscCharge, UnitMaster, PlatingMaster, MiscChargeMaster,
    DesignGroupMaster, ItemMaster, DepartmentMaster, StoneMaster,
    ArtisanMaster, DealerMaster, StaffMaster, CustomerMaster,
    RawMaterialMaster, ProcessMaster, PlatingPolishMaster, DesignMaster,
    SystemMaster, CompanyMaster, StoneSubMaster, DesignItemType
)


# -----------------------------
# Helper: unique code validator
# -----------------------------
def unique_code_validator(model, field_name, incoming_name, friendly_name):
    """
    Returns a serializer.validate function that checks uniqueness of `incoming_name`
    against model field `field_name`. `friendly_name` is used in the error key.
    """
    def _validate(self, data):
        code = data.get(incoming_name)
        if code is None:
            return data
        qs = model.objects.filter(**{field_name: code})
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                friendly_name: f"The code '{code}' already exists and cannot be reused."
            })
        return data
    return _validate

# -----------------------------
# Base Serializers (no FKs)
# -----------------------------




class MappingTCSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingTC
        fields = '__all__'
        read_only_fields = ('ID', 'Trancode')
        
        
        
class ColorMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Code")
        qs = ColorMaster.objects.filter(Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


class UnitMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Unit_Code")
        qs = UnitMaster.objects.filter(Unit_Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Unit_Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


class PlatingMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatingMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Code")
        qs = PlatingMaster.objects.filter(Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


class MiscChargeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiscChargeMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Code")
        qs = MiscChargeMaster.objects.filter(Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Misc_Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


class DesignGroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignGroupMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Code")
        qs = DesignGroupMaster.objects.filter(Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


class ItemMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Code")
        qs = ItemMaster.objects.filter(Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


class ArtisanMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Code")
        qs = ArtisanMaster.objects.filter(Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Artisan_Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


class DealerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealerMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Code")
        qs = DealerMaster.objects.filter(Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data

class CustomerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMaster
        fields = "__all__"


class PlatingPolishMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatingPolishMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Polish_Code")
        qs = PlatingPolishMaster.objects.filter(Polish_Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Polish_Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data


# -----------------------------
# Serializers with FKs
# -----------------------------





class ProcessMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessMaster
        fields = "__all__"

    def validate(self, data):
        code = data.get("Process_Code")
        qs = ProcessMaster.objects.filter(Process_Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Process_Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data



class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMaster
        fields = "__all__"
    def validate(self, data):
        code = data.get("Company_Code")
        qs = CompanyMaster.objects.filter(Company_Code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                "Company_Code": f"The code '{code}' already exists and cannot be reused."
            })
        return data





# -----------------------------
# StoneMaster (FK → UnitMaster)
# -----------------------------
class StoneMasterSerializer(serializers.ModelSerializer):
    ID_master = serializers.PrimaryKeyRelatedField(queryset=UnitMaster.objects.all())
    Unit_ID = serializers.SerializerMethodField()
    Unit_Code = serializers.SerializerMethodField()
    Unit_Description = serializers.SerializerMethodField()

    class Meta:
        model = StoneMaster
        fields = [
            "ID", "Code", "Description",
            "ID_master", "Unit_ID", "Unit_Code", "Unit_Description"
        ]

    def get_Unit_ID(self, obj):
        return obj.ID_master.Unit_ID if obj.ID_master else None

    def get_Unit_Code(self, obj):
        return obj.ID_master.Unit_Code if obj.ID_master else None

    def get_Unit_Description(self, obj):
        return obj.ID_master.Description if obj.ID_master else None



# -----------------------------
# StoneSubMaster (FK → StoneMaster, UnitMaster)
# -----------------------------
class StoneSubMasterSerializer(serializers.ModelSerializer):
    ID_Group = serializers.PrimaryKeyRelatedField(queryset=StoneMaster.objects.all())

    # Flatten StoneMaster
    ID = serializers.SerializerMethodField()
    Code = serializers.SerializerMethodField()
    Description = serializers.SerializerMethodField()

  

    class Meta:
        model = StoneSubMaster
        fields = [
            "Sub_ID", "Sub_Code", "Description", "Pcs", "Weight",
            "ID_Group", "ID", "Code", "Description",
        ]

    def get_ID(self, obj):
        return obj.ID_Group.ID if obj.ID_Group else None

    def get_Code(self, obj):
        return obj.ID_Group.Code if obj.ID_Group else None

    def get_Description(self, obj):
        return obj.ID_Group.Description if obj.ID_Group else None

    


# -----------------------------
# DepartmentMaster (FK → ProcessMaster)
# -----------------------------
class DepartmentMasterSerializer(serializers.ModelSerializer):
    ID_master = serializers.PrimaryKeyRelatedField(queryset=ProcessMaster.objects.all())
    Process_ID = serializers.SerializerMethodField()
    Process_Code = serializers.SerializerMethodField()
    Process_Description = serializers.SerializerMethodField()
    class Meta:
        model = DepartmentMaster
        fields = [
            "ID", "Code", "Description",
            "ID_master", "Process_ID", "Process_Code", "Process_Description"
        ]
    def get_Process_ID(self, obj):
        return obj.ID_master.Process_ID if obj.ID_master else None
    def get_Process_Code(self, obj):
        return obj.ID_master.Process_Code if obj.ID_master else None
    def get_Process_Description(self, obj):
        return obj.ID_master.Description if obj.ID_master else None


# -----------------------------
# StaffMaster (FK → ProcessMaster)
# -----------------------------
class StaffMasterSerializer(serializers.ModelSerializer):
    ID_master = serializers.PrimaryKeyRelatedField(queryset=ProcessMaster.objects.all())
    Process_ID = serializers.SerializerMethodField()
    Process_Code = serializers.SerializerMethodField()
    Process_Description = serializers.SerializerMethodField()

    class Meta:
        model = StaffMaster
        fields = [
            "Staff_ID", "Staff_Code", "Staff_Name", "Address1", "Address2", "Address3", "Contact",
            "ID_master", "Process_ID", "Process_Code", "Process_Description"
        ]

    def get_Process_ID(self, obj):
        return obj.ID_master.Process_ID if obj.ID_master else None

    def get_Process_Code(self, obj):
        return obj.ID_master.Process_Code if obj.ID_master else None

    def get_Process_Description(self, obj):
        return obj.ID_master.Description if obj.ID_master else None



# -----------------------------
# RawMaterialMaster (FK → SystemMaster)
# -----------------------------
class RawMaterialMasterSerializer(serializers.ModelSerializer):
    Metal_Type = serializers.PrimaryKeyRelatedField(queryset=SystemMaster.objects.all())
    System_ID = serializers.SerializerMethodField()
    System_Name = serializers.SerializerMethodField()
    Metal_Type_Label = serializers.SerializerMethodField()

    class Meta:
        model = RawMaterialMaster
        fields = [
            "Raw_ID", "Raw_Code", "Raw_Description", "Tolerance_Lower", "Tolerance_Upper",
            "Metal_Type", "System_ID", "System_Name", "Metal_Type_Label"
        ]

    def get_System_ID(self, obj):
        return obj.Metal_Type.id if obj.Metal_Type else None

    def get_System_Name(self, obj):
        return obj.Metal_Type.System_Name if obj.Metal_Type else None

    def get_Metal_Type_Label(self, obj):
        return obj.Metal_Type.get_Metal_Type_display() if obj.Metal_Type else None


# -----------------------------
# DesignMaster (FK → DesignGroupMaster, ItemMaster)
# -----------------------------
class DesignMasterSerializer(serializers.ModelSerializer):
    Design_Group = serializers.PrimaryKeyRelatedField(queryset=DesignGroupMaster.objects.all())
    ID_Item = serializers.PrimaryKeyRelatedField(queryset=ItemMaster.objects.all())

    # Flatten DesignGroup
    Design_Grp_ID = serializers.SerializerMethodField()
    Design_Grp_Code = serializers.SerializerMethodField()
    Design_Grp_Description = serializers.SerializerMethodField()

    # Flatten Item
    Item_ID = serializers.SerializerMethodField()
    Item_Code = serializers.SerializerMethodField()
    Item_Description = serializers.SerializerMethodField()

    class Meta:
        model = DesignMaster
        fields = [
            "DesignID", "Design_Code",  "Description",
            "Design_Group", "Design_Grp_ID", "Design_Grp_Code", "Design_Grp_Description",
            "ID_Item", "Item_ID", "Item_Code", "Item_Description",
            "Picture", "Gross_Weight", "Tolerance_Lower", "Tolerance_Upper"
        ]

    def get_Design_Grp_ID(self, obj):
        return obj.Design_Group.Design_Grp_ID if obj.Design_Group else None

    def get_Design_Grp_Code(self, obj):
        return obj.Design_Group.Design_Grp_Code if obj.Design_Group else None

    def get_Design_Grp_Description(self, obj):
        return obj.Design_Group.Description if obj.Design_Group else None

    def get_Item_ID(self, obj):
        return obj.ID_Item.Item_ID if obj.ID_Item else None

    def get_Item_Code(self, obj):
        return obj.ID_Item.Item_Code if obj.ID_Item else None

    def get_Item_Description(self, obj):
        return obj.ID_Item.Description if obj.ID_Item else None


# -----------------------------
# SystemMaster (FK → CompanyMaster)
# -----------------------------
class SystemMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemMaster
        fields = "__all__"




class SizeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeMaster
        fields = "__all__"

    validate = unique_code_validator(SizeMaster, "Code", "Code", "Code")
    
    
class ItemTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTypeMaster
        fields = "__all__"

    validate = unique_code_validator(ItemTypeMaster, "Code", "Code", "Code")



class StoneRateSettingMiscChargeSerializer(serializers.ModelSerializer):
    MisCharge_Name = serializers.CharField(source="ID_MiscCharge.Code", read_only=True)
    ID_Header = serializers.PrimaryKeyRelatedField(read_only=True)  # ✅ read-only to avoid "required" error
    class Meta:
        model = StoneRateSettingMiscCharge
        fields = ["ID", "ID_MiscCharge", "Amount", "MisCharge_Name","ID_Header"]


class StoneRateSettingSerializer(serializers.ModelSerializer):
    # Nested serializers or fields for displaying related values
    StoneM_Name = serializers.CharField(source="ID_StoneM.Code", read_only=True)
    StoneS_Name = serializers.CharField(source="ID_StoneS.Sub_Code", read_only=True)
    Color_Name = serializers.CharField(source="ID_Color.Code", read_only=True)

    Details = StoneRateSettingMiscChargeSerializer(many=True, required=False)

    class Meta:
        model = StoneRateSetting
        fields = [
            "ID",
            "ID_StoneM", "StoneM_Name",
            "ID_StoneS", "StoneS_Name",
            "ID_Color", "Color_Name",
            "Pcs",
            "Weight",
            "CP",
            "SP",
            "Details",
            "Tolerance_Upper", "Tolerance_Lower"
        ]

    def create(self, validated_data):
        details_data = validated_data.pop("Details", [])
        # Create header
        header = StoneRateSetting.objects.create(**validated_data)
        # Attach header ID to details
        for detail in details_data:
            StoneRateSettingMiscCharge.objects.create(ID_Header=header, **detail)
        return header

    def update(self, instance, validated_data):
        details_data = validated_data.pop("Details", None)

        # Update header fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            # Replace old details
            StoneRateSettingMiscCharge.objects.filter(ID_Header=instance).delete()
            for detail in details_data:
                StoneRateSettingMiscCharge.objects.create(ID_Header=instance, **detail)

        return instance




# -----------------------------
# DesignMaster & DesignDetail
# -----------------------------

class DesignDetailSerializer(serializers.ModelSerializer):
    Size_Name = serializers.CharField(source="ID_Size.Code", read_only=True)
    StoneM_Name = serializers.CharField(source="ID_StoneM.Code", read_only=True)
    StoneS_Name = serializers.CharField(source="ID_StoneS.Sub_Code", read_only=True)

    class Meta:
        model = DesignDetail
        fields = [
            "ID", "ID_Size", "Size_Name",
            "ID_StoneM", "StoneM_Name", "ID_StoneS", "StoneS_Name",
            "Pcs", "Weight"
        ]
        
class DesignItemTypeDetailSerializer(serializers.ModelSerializer):
    ItemType_Name = serializers.CharField(source="ID_ItemType.Code", read_only=True)

    class Meta:
        model = DesignItemType
        fields = [
            "ID", "ID_ItemType", "ItemType_Name","ID_Header","Approx_Gross_Weight"
        ]




class DesignMasterSerializer(serializers.ModelSerializer):
    Details = DesignDetailSerializer(many=True, required=False)
    dgm_name = serializers.CharField(source="Design_Group.Code", read_only=True)
    item_name = serializers.CharField(source="ID_master.Code", read_only=True)

    class Meta:
        model = DesignMaster
        fields = [
            "DesignID", "Design_Code",
            "Design_Description", "Design_Group", "ID_master",
            "Picture",  "Tolerance_Lower",
            "Tolerance_Upper", "Details","dgm_name","item_name"
        ]

    def create(self, validated_data):
        details_data = validated_data.pop("Details", [])
        itemtype_data = validated_data.pop("ItemTypeDetails", [])
        header = DesignMaster.objects.create(**validated_data)
        for detail in details_data:
            # print("✅ Creating DesignDetail:", detail)
            size=detail.get("ID_Size")
            # print("✅ Size ID:", size)
            try:
                size_instance = SizeMaster.objects.get(pk=size)
            except ObjectDoesNotExist:
                # print(f"❌ SizeMaster with ID {size} does not exist. Skipping this detail.")
                continue  # Skip creating this detail
            
            pcs = detail.get("Pcs")
            weight = detail.get("Weight")
            stone_m_instance = StoneMaster.objects.get(pk=detail["ID_StoneM"])
            stone_s_instance = StoneSubMaster.objects.get(pk=detail["ID_StoneS"])
           
            DesignDetail.objects.create(
                ID_Header=header,
                ID_StoneM=stone_m_instance,
                ID_StoneS=stone_s_instance,
                ID_Size=size_instance,
                Pcs=pcs,
                Weight=weight,
                )
        for detail in itemtype_data:
            # print("✅ Creating DesignItemTypeDetail:", detail)
            itemtype = detail.get("ID_ItemType")
            # print("✅ ItemType ID:", itemtype)
            try:
                itemtype_instance = ItemTypeMaster.objects.get(pk=itemtype)
            except ObjectDoesNotExist:
                # print(f"❌ ItemTypeMaster with ID {itemtype} does not exist. Skipping this detail.")
                continue  # Skip creating this detail
            approx_gross_weight = detail.get("Approx_Gross_Weight")
            DesignItemType.objects.create(
                ID_Header=header,
                ID_ItemType=itemtype_instance,
                Approx_Gross_Weight=approx_gross_weight
            )

        return header
