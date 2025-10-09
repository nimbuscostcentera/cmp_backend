from django.contrib import admin
from .models import (
    CompanyMaster, YearMaster, UserMaster, UnitMaster, StoneMaster,
    StoneSubMaster, ColorMaster, PlatingMaster, MiscChargeMaster,
    PlatingPolishMaster, ItemMaster, SystemMaster, RawMaterialMaster,
    DesignGroupMaster, DesignMaster, ProcessMaster, DepartmentMaster,
    ArtisanMaster, DealerMaster, StaffMaster, CustomerMaster
)
from .models import ApiTransactionMap

# Register all models with default admin
admin.site.register(CompanyMaster)
admin.site.register(YearMaster)
admin.site.register(UserMaster)
admin.site.register(UnitMaster)
admin.site.register(StoneMaster)
admin.site.register(StoneSubMaster)
admin.site.register(ColorMaster)
admin.site.register(PlatingMaster)
admin.site.register(MiscChargeMaster)
admin.site.register(PlatingPolishMaster)
admin.site.register(ItemMaster)
admin.site.register(SystemMaster)
admin.site.register(RawMaterialMaster)
admin.site.register(DesignGroupMaster)
admin.site.register(DesignMaster)
admin.site.register(ProcessMaster)
admin.site.register(DepartmentMaster)
admin.site.register(ArtisanMaster)
admin.site.register(DealerMaster)
admin.site.register(StaffMaster)
admin.site.register(CustomerMaster)



















# ////////////////////////////////////////////////
# SPECIAL DISPLAY:

# from django.contrib import admin
# from .models import (
#     CompanyMaster, YearMaster, UserMaster, UnitMaster, StoneMaster,
#     StoneSubMaster, ColorMaster, PlatingMaster, MiscChargeMaster,
#     PlatingPolishMaster, ItemMaster, SystemMaster, RawMaterialMaster,
#     DesignGroupMaster, DesignMaster, ProcessMaster, DepartmentMaster,
#     ArtisanMaster, DealerMaster, StaffMaster, CustomerMaster
# )

# @admin.register(CompanyMaster)
# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ("Company_Code", "Company_Name", "GSTIN", "Active", "Contact")
#     search_fields = ("Company_Code", "Company_Name", "GSTIN")
#     list_filter = ("Active",)

# @admin.register(YearMaster)
# class YearAdmin(admin.ModelAdmin):
#     list_display = ("Year_Code", "Start_Date", "End_Date", "active")
#     list_filter = ("active",)
#     search_fields = ("Year_Code",)

# @admin.register(UserMaster)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("User_Name", "Contact", "UType", "active")
#     list_filter = ("UType", "active")
#     search_fields = ("User_Name", "Contact")

# @admin.register(UnitMaster)
# class UnitAdmin(admin.ModelAdmin):
#     list_display = ("Unit_Code", "Description", "Conversion")
#     search_fields = ("Unit_Code", "Description")

# @admin.register(StoneMaster)
# class StoneAdmin(admin.ModelAdmin):
#     list_display = ("Stone_Code", "Description", "ID_Unit")
#     search_fields = ("Stone_Code", "Description")

# @admin.register(StoneSubMaster)
# class StoneSubAdmin(admin.ModelAdmin):
#     list_display = ("Sub_Code", "Description", "Pcs", "Weight", "ID_Group", "Unit")
#     search_fields = ("Sub_Code", "Description")

# @admin.register(ColorMaster)
# class ColorAdmin(admin.ModelAdmin):
#     list_display = ("Color_Code", "Description")
#     search_fields = ("Color_Code", "Description")

# @admin.register(PlatingMaster)
# class PlatingAdmin(admin.ModelAdmin):
#     list_display = ("Plating_Code", "Description")
#     search_fields = ("Plating_Code", "Description")

# @admin.register(MiscChargeMaster)
# class MiscChargeAdmin(admin.ModelAdmin):
#     list_display = ("Misc_Code", "Description")
#     search_fields = ("Misc_Code", "Description")

# @admin.register(PlatingPolishMaster)
# class PlatingPolishAdmin(admin.ModelAdmin):
#     list_display = ("Polish_Code", "Description", "Rate")
#     search_fields = ("Polish_Code", "Description")

# @admin.register(ItemMaster)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ("Item_Code", "Description")
#     search_fields = ("Item_Code", "Description")

# @admin.register(SystemMaster)
# class SystemAdmin(admin.ModelAdmin):
#     list_display = ("Metal_Type", "System_Name", "Company_Name")
#     search_fields = ("System_Name",)

# @admin.register(RawMaterialMaster)
# class RawMaterialAdmin(admin.ModelAdmin):
#     list_display = ("Raw_Code", "Description", "Metal_Type", "Tolerance_Lower", "Tolerance_Upper")
#     search_fields = ("Raw_Code", "Description")

# @admin.register(DesignGroupMaster)
# class DesignGroupAdmin(admin.ModelAdmin):
#     list_display = ("Design_Grp_Code", "Description")
#     search_fields = ("Design_Grp_Code", "Description")

# @admin.register(DesignMaster)
# class DesignAdmin(admin.ModelAdmin):
#     list_display = ("Design_Code", "Ref_Code", "Description", "Design_Group", "ID_Item", "Gross_Weight")
#     search_fields = ("Design_Code", "Ref_Code", "Description")

# @admin.register(ProcessMaster)
# class ProcessAdmin(admin.ModelAdmin):
#     list_display = ("Process_Code", "Description", "Execution_Days", "Design_Stock_Effect")
#     search_fields = ("Process_Code", "Description")
#     list_filter = ("Design_Stock_Effect",)

# @admin.register(DepartmentMaster)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ("Dept_Code", "Description", "ID_Process")
#     search_fields = ("Dept_Code", "Description")

# @admin.register(ArtisanMaster)
# class ArtisanAdmin(admin.ModelAdmin):
#     list_display = ("Artisan_Code", "Artisan_Name", "Contact")
#     search_fields = ("Artisan_Code", "Artisan_Name", "Contact")

# @admin.register(DealerMaster)
# class DealerAdmin(admin.ModelAdmin):
#     list_display = ("Dealer_Code", "Dealer_Name", "Contact")
#     search_fields = ("Dealer_Code", "Dealer_Name", "Contact")

# @admin.register(StaffMaster)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ("Staff_Code", "Staff_Name", "Contact", "ID_Process")
#     search_fields = ("Staff_Code", "Staff_Name", "Contact")

# @admin.register(CustomerMaster)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ("Customer_Name", "Contact", "ID_Type")
#     search_fields = ("Customer_Name", "Contact")
#     list_filter = ("ID_Type",)
