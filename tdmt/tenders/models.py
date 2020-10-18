from computedfields.models import ComputedFieldsModel, computed
from django.db import models
from simple_history.models import HistoricalRecords
from tinymce import models as tinymce_models
from tdmt.users.models import User


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
        ordering = ["updated_at"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

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


class Client(ComputedFieldsModel):
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    name = models.CharField(max_length=256, null=True)
    surname = models.CharField(max_length=256, null=True)
    birthday = models.CharField(max_length=256, null=True)
    age = models.IntegerField(null=True)
    gender_code = models.CharField(max_length=256, null=True)
    directory = models.CharField(max_length=256, null=True)
    aMRG_eop = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    aCSH_eop = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    aCRD_eop = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    pCUR_eop = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    pCRD_eop = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    pSAV_eop = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    pDEP_eop = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    sWork_S = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    tPOS_S = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # @computed(models.BooleanField(null=True), depends=['name'])
    # def isPremium(self):
    #     # if (self.sWork_S > 250000 and self.tPOS_S > 50000) or \
    #     #         (self.pCRD_eop + self.pCUR_eop + self.pDEP_eop + self.pSAV_eop > 2000000) or \
    #     #         (self.pCRD_eop + self.pCUR_eop + self.pDEP_eop + self.pSAV_eop > 1000000 and self.tPOS_S > 50000):
    #     #     return 1
    #     # else:
    #     #     return 0
    #     return self.name == self.name

    def __str__(self):
        return str(self.id)


class MCC(models.Model):
    GroupName = models.CharField(max_length=256, null=True)
    Description = models.CharField(max_length=256, null=True)

    def __str__(self):
        return str(self.Description)


class Transaction(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    TRANSACTION_DT = models.CharField(max_length=256, null=True)
    MCC_KIND_CD = models.CharField(max_length=256, null=True)
    MCC_CD = models.ForeignKey(MCC, on_delete=models.SET_NULL, null=True)
    CARD_AMOUNT_EQV_CBR = models.DecimalField(max_digits=30, decimal_places=2, null=True)

    def __str__(self):
        return str(self.CARD_AMOUNT_EQV_CBR) + ' ' + str(self.MCC_KIND_CD)
