from django.db import models
from django.forms import ValidationError

# Create your models here.
# All Codes to be Non-Editable, all mandatory fields should have '*'
class CompanyMaster(models.Model):
    Company_ID=models.AutoField(primary_key=True)
    Company_Code=models.CharField(max_length=15,unique=True)
    Company_Name=models.CharField(max_length=50)
    GSTIN=models.CharField(max_length=15)
    Active=models.BooleanField(default=True)
    Address=models.CharField(max_length=255,blank=True)
    Contact=models.CharField(max_length=30,blank=True)

    def __str__(self):
        return self.Company_Code

class YearMaster(models.Model):
    Year_ID=models.AutoField(primary_key=True)
    Year_Code=models.CharField(max_length=10,unique=True)
    Start_Date=models.DateField(auto_now=True)
    End_Date=models.DateField(auto_now=True)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.Year_Code

class UserMaster(models.Model):
    User_ID=models.AutoField(primary_key=True)
    User_Name=models.CharField(max_length=255)
    Contact=models.CharField(max_length=30)
    Password=models.CharField(max_length=255)
    TYPE_A='S'
    TYPE_B='A'
    TYPE_C='U'
    USER_CHOICES=[
        (TYPE_A,'SuperUser'),
        (TYPE_B,'Admin'),
        (TYPE_C,'User'),
    ]
    UType=models.CharField(max_length=1,choices=USER_CHOICES)
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.User_Name

# All fields are mandatory:
class UnitMaster(models.Model):
    Unit_ID=models.AutoField(primary_key=True)
    Unit_Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)
    Conversion=models.DecimalField(max_digits=10,decimal_places=3)

    def __str__(self):
        return self.Unit_Code

class StoneMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)
    ID_master=models.ForeignKey(UnitMaster,on_delete=models.PROTECT)
    def __str__(self):
        return self.Code



class StoneSubMaster(models.Model):
    Sub_ID=models.AutoField(primary_key=True)
    Sub_Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)
    Pcs=models.IntegerField()
    Weight=models.DecimalField(max_digits=6,decimal_places=3)
    ID_Group=models.ForeignKey(StoneMaster,on_delete=models.PROTECT)

    def __str__(self):
        return self.Sub_Code

# Done
class ColorMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)

    def __str__(self):
        return self.Code

class PlatingMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)

    def __str__(self):
        return self.Code

# Doubt: amount(float-<6.2>) *********************************************************************
class MiscChargeMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)

    def __str__(self):
        return self.Code

class PlatingPolishMaster(models.Model):
    Polish_ID=models.AutoField(primary_key=True)
    Polish_Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)
    Rate=models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.Polish_Code

class ItemMaster(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Code = models.CharField(max_length=6, unique=True)
    Description = models.CharField(max_length=15)
    Size = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.Code

# Doubt: About the structure...No System ID*********************************************
class SystemMaster(models.Model):
    TYPE_A='P'
    TYPE_B='B'
    TYPE_C='A'
    TYPE_D='M'
    TYPE_E='S'
    TYPE_F='O'
    METAL_CHOICES=[
        (TYPE_A,'Pure'),
        (TYPE_B,'Brass'),
        (TYPE_C,'Alloy'),
        (TYPE_D,'Model'),
        (TYPE_E,'Scrap'),
        (TYPE_F,'Others'),
    ]
    Metal_Type=models.CharField(max_length=1,choices=METAL_CHOICES)
    System_Name = models.CharField(max_length=255,default='Default System')  #fixed
    Company_Name=models.ForeignKey(CompanyMaster,on_delete=models.PROTECT)
    def __str__(self):
        return self.System_Name

# All are mandatory except “Tolerance Limit” 
class RawMaterialMaster(models.Model):
    Raw_ID=models.AutoField(primary_key=True)
    Raw_Code=models.CharField(max_length=6,unique=True)
    Raw_Description=models.CharField(max_length=15)
    Tolerance_Lower=models.DecimalField(max_digits=6,decimal_places=3,null=True,blank=True)
    Tolerance_Upper=models.DecimalField(max_digits=6,decimal_places=3,null=True,blank=True)
    Metal_Type=models.ForeignKey(SystemMaster,on_delete=models.PROTECT)
    def __str__(self):
        return self.Raw_Code
    
    
class DesignGroupMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)

    def __str__(self):
        return self.Code



class ProcessMaster(models.Model):
    Process_ID=models.AutoField(primary_key=True)
    Process_Code=models.CharField(max_length=15,unique=True)
    Description=models.CharField(max_length=30)
    Process_Serial = models.IntegerField(default=0)
    Execution_Days=models.IntegerField()
    Design_Stock_Effect=models.BooleanField(default=False)

    def __str__(self):
        return self.Process_Code

class DepartmentMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Description=models.CharField(max_length=15)
    ID_master=models.ForeignKey(ProcessMaster,on_delete=models.PROTECT)
    def __str__(self):
        return self.Code

# All are mandatory except address,contact
class ArtisanMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Name=models.CharField(max_length=100)
    Address1=models.CharField(max_length=255,null=True,blank=True)
    Address2=models.CharField(max_length=255,null=True,blank=True)
    Address3=models.CharField(max_length=255,null=True,blank=True)
    Contact=models.CharField(max_length=30,null=True,blank=True)
    def __str__(self):
        return self.Code
class DealerMaster(models.Model):
    ID=models.AutoField(primary_key=True)
    Code=models.CharField(max_length=6,unique=True)
    Name=models.CharField(max_length=100)
    Address1=models.CharField(max_length=255,blank=True)
    Address2=models.CharField(max_length=255,blank=True)
    Address3=models.CharField(max_length=255,blank=True)
    Contact=models.CharField(max_length=30,blank=True)
    def __str__(self):
        return self.Code


# All are mandatory except address,contact.
class StaffMaster(models.Model):
    Staff_ID=models.AutoField(primary_key=True)
    Staff_Code=models.CharField(max_length=6,unique=True)
    Staff_Name=models.CharField(max_length=100)
    Address1=models.CharField(max_length=255,blank=True)
    Address2=models.CharField(max_length=255,blank=True)
    Address3=models.CharField(max_length=255,blank=True)
    Contact=models.CharField(max_length=30,blank=True)
    ID_master=models.ForeignKey(ProcessMaster,on_delete=models.PROTECT)
    def __str__(self):
        return self.Staff_Code

class CustomerMaster(models.Model):
    Customer_ID=models.AutoField(primary_key=True)
    # Check: Customer Code(Not Reqd)
    Customer_Name=models.CharField(max_length=100)
    # All are mandatory except address’s,contact.
    Address1=models.CharField(max_length=255,blank=True,null=True)
    Address2=models.CharField(max_length=255,blank=True,null=True)
    Address3=models.CharField(max_length=255,blank=True,null=True)
    Contact=models.CharField(max_length=30,blank=True,null=True)
    TYPE_A=1
    TYPE_B=2
    ID_CHOICES=[
        (TYPE_A,'Self'),
        (TYPE_B,'Customer'),
    ]
    ID_Type=models.CharField(max_length=1,choices=ID_CHOICES,default=TYPE_B)

    def __str__(self):
        return self.Customer_Name



# Mapping Table:
class ApiTransactionMap(models.Model):
    transaction_code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    endpoint = models.CharField(max_length=200)  # e.g. /colormaster/

    def __str__(self):
        return f"{self.transaction_code} -> {self.endpoint}"
    
    

class SizeMaster(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Code = models.CharField(max_length=6, unique=True)
    Description = models.CharField(max_length=30)

    def __str__(self):
        return self.Code
    
    
    
class ItemTypeMaster(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Code = models.CharField(max_length=6, unique=True)
    Description = models.CharField(max_length=30)

    def __str__(self):
        return self.Code    



# ---------------------------
# Stone Rate Setting
# ---------------------------
class StoneRateSetting(models.Model):
    ID = models.BigAutoField(primary_key=True)
    ID_StoneM = models.ForeignKey(StoneMaster, on_delete=models.PROTECT)
    ID_StoneS = models.ForeignKey(StoneSubMaster, on_delete=models.PROTECT)
    ID_Color = models.ForeignKey(ColorMaster, on_delete=models.PROTECT)
    Pcs = models.IntegerField()
    Weight = models.DecimalField(max_digits=10, decimal_places=3)
    CP = models.DecimalField(max_digits=8, decimal_places=2)
    SP = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.ID)
 

class StoneRateSettingMiscCharge(models.Model):
    ID = models.BigAutoField(primary_key=True)
    ID_Header = models.ForeignKey(
        StoneRateSetting,
        on_delete=models.CASCADE,
        db_column="ID_Header"   # 👈 Forces column name
    )
    ID_MiscCharge = models.ForeignKey(MiscChargeMaster, on_delete=models.PROTECT)
    Amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.ID)
    
    

# Header: All are mandatory except “Ref Code”, ”Tolerance Limit”
# Detail: Before Item there has “Srl” column. If “Item” OR “Stone Main” OR “Stone Sub”   
#         exists then whole line mandatory rather line must not be saved.                        
# “Srl” column NE auto increase. 
class DesignMaster(models.Model):
    DesignID = models.BigAutoField(primary_key=True)
    Design_Code = models.CharField(max_length=15, unique=True)
    Design_Description = models.CharField(max_length=30)
    Design_Group = models.ForeignKey(DesignGroupMaster, on_delete=models.PROTECT)
    ID_master = models.ForeignKey(ItemMaster, on_delete=models.PROTECT)
    ID_StoneM = models.ForeignKey(StoneMaster, on_delete=models.PROTECT,default=1)
    ID_StoneS = models.ForeignKey(StoneSubMaster, on_delete=models.PROTECT,default=1)
    Pcs = models.IntegerField(default=1)
    Weight = models.DecimalField(max_digits=9, decimal_places=3, editable=False,default=0)
    Picture = models.ImageField(upload_to='design_pictures/', null=True, blank=True)
    Gross_Weight = models.DecimalField(max_digits=9, decimal_places=3)
    Tolerance_Lower = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    Tolerance_Upper = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ID_StoneS:
            self.Weight = self.ID_StoneS.Weight
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Design_Code

    class Meta:
        ordering = ["DesignID"]  # Default ordering by DesignID
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['ID_master', 'ID_StoneM', 'ID_StoneS'],
    #             name='unique_master_stone_substone'
    #         )
    #     ]



class DesignDetail(models.Model):
    ID = models.BigAutoField(primary_key=True)
    ID_Header = models.ForeignKey(DesignMaster, on_delete=models.CASCADE,related_name="Details",db_column="ID_Header" )
    ID_Size = models.ForeignKey(SizeMaster, on_delete=models.PROTECT,default=0)
    ID_StoneM = models.ForeignKey(StoneMaster, on_delete=models.PROTECT)
    ID_StoneS = models.ForeignKey(StoneSubMaster, on_delete=models.PROTECT)
    Pcs = models.IntegerField()
    Weight = models.DecimalField(max_digits=10, decimal_places=3)

    def clean(self):
        """
        Custom validation:
        ID_Size is mandatory if related ItemMaster has Size=True
        """
        item_master = self.ID_Header.ID_master  # DesignMaster has FK -> ItemMaster
        if item_master.Size and not self.ID_Size:
            raise ValidationError({"ID_Size": "Size is required because the ItemMaster has Size checked."})

    def __str__(self):
        return str(self.ID)



class DesignItemType(models.Model):
    ID = models.BigAutoField(primary_key=True)
    ID_Header = models.ForeignKey(DesignMaster, on_delete=models.CASCADE,related_name="ItemTypeDetails")
    Approx_Gross_Weight = models.DecimalField(max_digits=10, decimal_places=3)
    ID_ItemType = models.ForeignKey(ItemTypeMaster, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.ID)