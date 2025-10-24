from django.db import models


class SetupInfo(models.Model):
    """
    This model stores system-wide configuration and control flags.
    """
    ID = models.BigAutoField(primary_key=True)

    # Reminder days field is boolean on/off:
    # ON -> default; if ON then auto date fetch, if OFF then manual entry.
    ReminderDays = models.BooleanField(
        default=True,
        help_text="If True, reminder days are auto-fetched; if False, entry must be manual."
    )

    # AutoVouDate field is on/off (default ON). If ON, allows negative value.
    AutoVouDate = models.BooleanField(
        default=True,
        help_text="If True, auto-fetch voucher date; otherwise manual entry required."
    )

    # If True → allows negative stone stock
    NegativeStoneStock = models.BooleanField(
        default=False,
        help_text="If True, allows negative stone stock."
    )

    # If True → allows negative raw material stock
    NegativeRawMaterial = models.BooleanField(
        default=False,
        help_text="If True, allows negative raw material stock."
    )
    

    # If True → enables stone issue feature
    OrderStoneValid = models.BooleanField(
        default=False,
        help_text="If True, enables the stone issue feature."
    )
    # :white_tick: New Field: Voucher Number control
    AutoVoucher = models.BooleanField(
        default=False,
        help_text=(
            "If False → Auto mode (voucher number generated automatically, user cannot edit). "
            "If True → Auto + Manual (user can override voucher number)."
        )
    )

    def __str__(self):
        return f"Setup Configuration (ID: {self.ID})"

    class Meta:
        verbose_name = "Setup Information"
        verbose_name_plural = "Setup Information"


class ProcessWiseControl(models.Model):
    """
    This model defines process-level visibility and mandatory settings.
    """
    ID = models.BigAutoField(primary_key=True)

    # Uncomment when ProcessMaster is defined
    # ID_Process = models.ForeignKey('masters.ProcessMaster', on_delete=models.PROTECT)

    ControlName = models.CharField(
        max_length=255,
        help_text="Name of the control associated with the process."
    )

    Visible = models.BooleanField(
        default=False,
        help_text="If True, control is visible for the process."
    )

    Mandatory = models.BooleanField(
        default=False,
        help_text="If True, control is mandatory for the process."
    )

    def __str__(self):
        return self.ControlName

    class Meta:
        verbose_name = "Process Wise Control"
        verbose_name_plural = "Process Wise Controls"
