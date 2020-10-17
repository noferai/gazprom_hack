from computedfields.models import ComputedFieldsModel
from django.db import models
from simple_history.models import HistoricalRecords
from tinymce import models as tinymce_models


class StateModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["stype", "name"]

    STATE_UNSTARTED = 0
    STATE_STARTED = 1
    STATE_DONE = 2
    STATE_KP = 3

    STATE_TYPES = ((STATE_UNSTARTED, "Unstarted"), (STATE_STARTED, "Started"), (STATE_DONE, "Done"), (STATE_KP, "KP"))

    slug = models.SlugField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    stype = models.PositiveIntegerField(db_index=True, choices=STATE_TYPES, default=STATE_UNSTARTED)

    def __str__(self):
        return self.name


class TaskState(StateModel):
    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказа"


class Task(ComputedFieldsModel):
    class Meta:
        ordering = ["date"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    date = models.DateField("Дата")
    state = models.ForeignKey(TaskState, on_delete=models.SET_NULL, null=True, verbose_name="Статус")
    comment = tinymce_models.HTMLField("Комментарий", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    history = HistoricalRecords()

    def is_done(self):
        if self.state.stype == StateModel.STATE_DONE:
            return True
        return False

    def is_started(self):
        if self.state.stype == StateModel.STATE_STARTED:
            return True
        return False

    def is_unstarted(self):
        if self.state.stype == StateModel.STATE_UNSTARTED:
            return True
        return False

    def is_kp(self):
        if self.state.stype == StateModel.STATE_KP:
            return True
        return False


class Client(models.Model):
    client_id = models.BigIntegerField()
    age = models.IntegerField()
    gender_code = models.CharField(max_length=1)
    directory = models.CharField(max_length=256)
    aMRG_eop = models.DecimalField(max_digits=30, decimal_places=2)
    aCSH_eop = models.DecimalField(max_digits=30, decimal_places=2)
    aCRD_eop = models.DecimalField(max_digits=30, decimal_places=2)
    pCUR_eop = models.DecimalField(max_digits=30, decimal_places=2)
    pCRD_eop = models.DecimalField(max_digits=30, decimal_places=2)
    pSAV_eop = models.DecimalField(max_digits=30, decimal_places=2)
    pDEP_eop = models.DecimalField(max_digits=30, decimal_places=2)
    sWork_S = models.DecimalField(max_digits=30, decimal_places=2)
    tPOS_S = models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self):
        return str(self.client_id)


class Transaction(models.Model):
    client_id = models.BigIntegerField()
    TRANSACTION_DT = models.DateField()
    MCC_KIND_CD = models.CharField(max_length=256)
    MCC_CD = models.DecimalField(max_digits=4, decimal_places=0)
    CARD_AMOUNT_EQV_CBR = models.DecimalField(max_digits=30, decimal_places=2)


class MCC(models.Model):
    MCC_CD = models.DecimalField(max_digits=4, decimal_places=0)
    GroupName = models.CharField(max_length=256)
    Description = models.CharField(max_length=256)
