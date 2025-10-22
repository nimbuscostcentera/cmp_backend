# models.py
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db.models import Max
from decimal import Decimal
from django.apps import apps
# NOTE: This file assumes it sits in your "opening" app (or similar),
# and references master models in 'masters' app (as you provided).

DR_CR_CHOICES = (
    ('DR', 'Dr'),
    ('CR', 'Cr'),
)


def next_srl(model_cls):
    max_srl = model_cls.objects.aggregate(m=Max('Srl'))['m']
    return (max_srl or 0) + 1


# -------------------------------
# TAB 1 - Vendor Opening (Raw Material)
# -------------------------------
class OpeningVendorRawMaterial(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Srl = models.PositiveIntegerField(editable=False)
    VendorGroup = models.ForeignKey('masters.VendorGroupMaster', on_delete=models.PROTECT)
    Vendor = models.ForeignKey('masters.VendorMaster', on_delete=models.PROTECT)
    RawMaterial = models.ForeignKey('masters.RawMaterialMaster', on_delete=models.PROTECT)
    Qty = models.DecimalField(max_digits=7, decimal_places=3)
    DrCr = models.CharField(max_length=2, choices=DR_CR_CHOICES)

    class Meta:
        db_table = 'Opening_Vendor_RawMaterial'
        unique_together = (('Vendor', 'RawMaterial'),)
        ordering = ('Srl',)

    def clean(self):
        if any([self.VendorGroup, self.Vendor, self.RawMaterial, self.Qty, self.DrCr]):
            if not (self.VendorGroup and self.Vendor and self.RawMaterial and self.Qty is not None and self.DrCr):
                raise ValidationError("All fields are mandatory if any value is entered.")

    def save(self, *args, **kwargs):
        if self.DrCr == 'DR':
            self.Qty = abs(self.Qty)
        elif self.DrCr == 'CR':
            self.Qty = -abs(self.Qty)

        if not self.Srl:
            with transaction.atomic():
                self.Srl = next_srl(OpeningVendorRawMaterial)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


# -------------------------------
# TAB 2 - Self Opening (Raw Material)
# -------------------------------
class OpeningRawMaterial(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Srl = models.PositiveIntegerField(editable=False)
    Department = models.ForeignKey('masters.DepartmentMaster', on_delete=models.PROTECT)
    RawMaterial = models.ForeignKey('masters.RawMaterialMaster', on_delete=models.PROTECT)
    Qty = models.DecimalField(max_digits=7, decimal_places=3)
    DrCr = models.CharField(max_length=2, choices=DR_CR_CHOICES, default='DR')

    class Meta:
        db_table = 'Opening_RawMaterial'
        unique_together = (('Department', 'RawMaterial'),)
        ordering = ('Srl',)

    def clean(self):
        if any([self.Department, self.RawMaterial, self.Qty, self.DrCr]):
            if not (self.Department and self.RawMaterial and self.Qty is not None and self.DrCr):
                raise ValidationError("All fields are mandatory if any value is entered.")

    def save(self, *args, **kwargs):
        if self.DrCr == 'DR':
            self.Qty = abs(self.Qty)
        elif self.DrCr == 'CR':
            self.Qty = -abs(self.Qty)

        if not self.Srl:
            with transaction.atomic():
                self.Srl = next_srl(OpeningRawMaterial)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


# -------------------------------
# TAB 3A - Vendor Stone Opening
# -------------------------------
class VendorStoneOpening(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Srl = models.PositiveIntegerField(editable=False)
    VendorGroup = models.ForeignKey('masters.VendorGroupMaster', on_delete=models.PROTECT)
    Vendor = models.ForeignKey('masters.VendorMaster', on_delete=models.PROTECT)
    StoneMain = models.ForeignKey('masters.StoneMaster', on_delete=models.PROTECT)
    StoneSub = models.ForeignKey('masters.StoneSubMaster', on_delete=models.PROTECT)
    Color = models.ForeignKey('masters.ColorMaster', on_delete=models.PROTECT)
    Pcs = models.IntegerField()
    Qty = models.DecimalField(max_digits=10, decimal_places=3)
    DrCr = models.CharField(max_length=2, choices=DR_CR_CHOICES)

    class Meta:
        db_table = 'Vendor_Stone_Opening'
        unique_together = (('Vendor', 'StoneMain', 'StoneSub', 'Color'),)
        ordering = ('Srl',)

    def clean(self):
        if not (self.VendorGroup and self.Vendor and self.StoneMain and self.StoneSub and self.Color and self.Pcs and self.DrCr):
            raise ValidationError("All fields are mandatory for Vendor Stone Opening.")

    def save(self, *args, **kwargs):
        if self.DrCr == 'DR':
            self.Qty = abs(self.Qty)
        elif self.DrCr == 'CR':
            self.Qty = -abs(self.Qty)

        if not self.Srl:
            with transaction.atomic():
                self.Srl = next_srl(VendorStoneOpening)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


# -------------------------------
# TAB 3 - Self Stone Opening
# -------------------------------
class SelfStoneOpening(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Srl = models.PositiveIntegerField(editable=False)
    Department = models.ForeignKey('masters.DepartmentMaster', on_delete=models.PROTECT)
    StoneMain = models.ForeignKey('masters.StoneMaster', on_delete=models.PROTECT)
    StoneSub = models.ForeignKey('masters.StoneSubMaster', on_delete=models.PROTECT)
    Color = models.ForeignKey('masters.ColorMaster', on_delete=models.PROTECT)
    Pcs = models.IntegerField()
    Qty = models.DecimalField(max_digits=10, decimal_places=3)
    DrCr = models.CharField(max_length=2, choices=DR_CR_CHOICES)

    class Meta:
        db_table = 'Self_Stone_Opening'
        unique_together = (('Department', 'StoneMain', 'StoneSub', 'Color'),)
        ordering = ('Srl',)

    def save(self, *args, **kwargs):
        if self.DrCr == 'DR':
            self.Qty = abs(self.Qty)
        elif self.DrCr == 'CR':
            self.Qty = -abs(self.Qty)
        if not self.Srl:
            with transaction.atomic():
                self.Srl = next_srl(SelfStoneOpening)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


# --------------------------------------------------
# LAYOUT C: Design + Stone + Color (same as before)
# --------------------------------------------------
class OpeningDesignStock(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Trancode = models.CharField(max_length=10, default='OPE', editable=False)
    Srl = models.PositiveIntegerField(editable=False)
    ID_Department = models.ForeignKey('masters.DepartmentMaster', on_delete=models.CASCADE)
    ID_Design = models.ForeignKey('masters.DesignMaster', on_delete=models.CASCADE)
    ID_ItemType = models.ForeignKey('masters.ItemTypeMaster', on_delete=models.CASCADE)
    ID_Item = models.ForeignKey('masters.ItemMaster', on_delete=models.CASCADE)
    ID_Size = models.ForeignKey('masters.SizeMaster', on_delete=models.CASCADE, null=True, blank=True)
    Pcs = models.IntegerField()
    GWeight = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    ColorS = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'Opening_Design_Stock'
        unique_together = (('ID_Department', 'ID_Design', 'ID_ItemType', 'ID_Item', 'ID_Size'),)
        ordering = ('Srl',)

    def save(self, *args, **kwargs):
        if not self.Srl:
            with transaction.atomic():
                self.Srl = next_srl(OpeningDesignStock)
        # No automatic GWeight/ColorS computation here
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.Srl} - {self.Design} - {self.Item} - {self.ColorS}"


class OpeningDesignStockStone(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Header = models.ForeignKey(OpeningDesignStock, on_delete=models.CASCADE, related_name='stones')
    ID_StoneM = models.ForeignKey('masters.StoneMaster', on_delete=models.CASCADE)
    ID_StoneS = models.ForeignKey('masters.StoneSubMaster', on_delete=models.CASCADE)
    ID_Color = models.ForeignKey('masters.ColorMaster', on_delete=models.CASCADE)
    Pcs = models.IntegerField()
    Weight = models.DecimalField(max_digits=12, decimal_places=3)
    PhysicalPcs = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Opening_Design_Stock_Stone'
        unique_together = (('Header', 'ID_StoneM', 'ID_StoneS', 'ID_Color'),)

    def clean(self):
        if self.PhysicalPcs is not None and self.PhysicalPcs > self.Pcs:
            raise ValidationError("PhysicalPcs cannot exceed Pcs.")


class OpeningDesignStockColor(models.Model):
    ID = models.BigAutoField(primary_key=True)
    Header = models.ForeignKey(OpeningDesignStock, on_delete=models.CASCADE, related_name='colors')
    Color = models.ForeignKey('masters.ColorMaster', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Opening_Design_Stock_Color'
        unique_together = (('Header', 'Color'),)
