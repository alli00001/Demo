from datetime import datetime
from django.db import models
from django.utils import timezone

def convertDate(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return "Invalid date format"

class ScopeOfWork(models.Model):
    scopeOfWork = models.CharField(max_length=100, default="", blank=True)
    qtyActual = models.IntegerField(default=0, blank=True)
    qtyBoq = models.IntegerField(default=0, blank=True)
    unitPrice = models.IntegerField(default=0, blank=True)
    totalActual = models.IntegerField(default=0, blank=True)
    totalBoq = models.IntegerField(default=0, blank=True)
    remarks = models.CharField(max_length=100, default="", blank=True)

    # Additional for Material n OC
    unit = models.CharField(max_length=100, default="", blank=True)



    def __str__(self) -> str:
        return self.scopeOfWork

class Deduction(models.Model):
    deductOrAddition = models.CharField(max_length=100, default="", blank=True)
    deductionAmount = models.FloatField(default = 0, blank = True)
    deductionRemarks = models.CharField(max_length=100, default="", blank=True)


    def __str__(self) -> str:
        returnString = self.deductOrAddition+'/'+'/'+self.deductionRemarks
        return returnString

class Payment(models.Model):
    pType = models.CharField(max_length=100, default="", blank=True)
    pPercentage = models.CharField(max_length=100, default="", blank=True)
    pAmount = models.IntegerField(default = 0, blank = True)
    pStatus = models.CharField(max_length=100, default="", blank=True)
    pDate = models.DateField(blank = True,  default=timezone.now)


    def __str__(self) -> str:
        returnString = self.pType+'/'+ self.pPercentage + '/'+str(self.pAmount) + '/' + self.pStatus
        return returnString
      
class WorkOrder(models.Model):
    #Privilage Check
    company = models.CharField(blank = True, max_length = 100, default ="")
    pricing_type = models.CharField(blank = True, max_length = 100, default ="")
    ceoCheck = models.BooleanField(default = False)
    rightHandCheck = models.BooleanField(default = False)
    personalAssistantCheck = models.BooleanField(default = False)
    financeCheck = models.BooleanField(default = False)
    extendable = models.BooleanField(default = False)
    remarksOverview = models.CharField(blank = True, max_length = 100, default ="")

    #General Information Table
    wo_date = models.DateField(blank = True, default=timezone.now)
    shortdate = models.CharField(max_length=100, blank = True, default = "")
    wo_number = models.CharField(max_length=100, blank = True, default = "")
    request_by = models.CharField(max_length = 100, blank = True, default = "")
    category = models.CharField(max_length=100, blank = True, default = "")
    project = models.CharField(max_length=100, blank = True, default = "")
    bank = models.CharField(max_length=100, blank = True, default = "")
    customer = models.CharField(max_length=100, blank = True, default = "")
    account_name = models.CharField(max_length=100, blank = True, default = "")
    department = models.CharField(max_length=100, blank = True, default = "")
    account_number = models.CharField(max_length=100, blank = True, default = "")
    region = models.CharField(max_length=100, blank = True, default = "" )
    phone_number = models.CharField(max_length=100, blank = True, default = "")
    city = models.CharField(max_length=100, blank = True, default = "")
    npwp = models.CharField(max_length=100, blank = True, default = "")

    # Cluster Name
    clusterName = models.CharField(max_length = 100 ,default ="", blank = True)
    siteId = models.CharField(max_length = 100,default ="", blank = True)
    type = models.CharField(max_length =100 , default ="", blank = True)
    workType = models.CharField(max_length =100 , default ="", blank = True)
    hp = models.CharField(max_length = 100,default ="", blank = True)
    odbId = models.CharField(max_length = 100,default ="", blank = True)
    suffixId = models.CharField(max_length = 100,default ="", blank = True)


    # Scope of Work
    workOrder = models.ManyToManyField(ScopeOfWork, blank = True)
    grandTotalActual = models.FloatField(default = 0, blank = True)
    grandTotalBoq = models.FloatField(default = 0, blank = True)

    # Donation Scope
    hpD = models.FloatField(default = 0, blank = True, )
    amountD = models.FloatField(default = 0, blank = True)
    unitPriceD =  models.FloatField(default = 0, blank = True)
    remarkD =  models.CharField(max_length = 100,default ="", blank = True)


    # Payment Table
    remarks1 = models.CharField(max_length = 100,default ="", blank = True)
    remarks2 = models.CharField(max_length = 100,default ="", blank = True)

    totalAmount = models.FloatField(default = 0, blank = True)


    paymentTerm = models.CharField(max_length = 100,default ="", blank = True)
    termPercentage = models.CharField(max_length = 100,default ="", blank = True)
    termAmount = models.FloatField(default = 0, blank = True)
    termRemark = models.CharField(max_length = 100,default ="", blank = True)

    paymentTax = models.CharField(max_length = 100,default ="", blank = True)
    taxPercentage = models.CharField(max_length = 100,default ="", blank = True)
    taxAmount = models.FloatField(default = 0, blank = True)
    taxRemark = models.CharField(max_length = 100,default ="", blank = True)

    deductions = models.ManyToManyField(Deduction, blank=True)

    finalGrandTotal = models.FloatField(default = 0, blank = True)

    # Payment 
    paymentInformation = models.ManyToManyField(Payment, blank=True)
    
    # MP DOCUMENT
    team_list = models.FileField(upload_to='team_list/' , blank=True, null=True)
    picture_of_team = models.FileField(upload_to='picture_of_team/' , blank=True, null=True)
    checklist_boq_actual_attachment = models.FileField(upload_to='checklist_boq_actual_attachment/' , blank=True, null=True)
    cover_acceptance_attachment = models.FileField(upload_to='cover_acceptance_attachment/' , blank=True, null=True)
    cover_opm_attachment = models.FileField(upload_to='cover_opm_attachment/' , blank=True, null=True)
    fac_certificate = models.FileField(upload_to='fac_certificate/' , blank=True, null=True)
    no_issue_agreement = models.FileField(upload_to='no_issue_agreement/' , blank=True, null=True)

    # DONATION DOCUMENT
    capture_approval = models.FileField(upload_to='capture_approval/' , blank=True, null=True)
    capture_drm = models.FileField(upload_to='capture_drm/' , blank=True, null=True)
    bak = models.FileField(upload_to='bak/' , blank=True, null=True)
    surat_izin =  models.CharField(max_length =100, default ="", blank = True)
    bap_open =  models.CharField(max_length =100, default ="", blank = True)
    form_survey =  models.CharField(max_length =100, default ="", blank = True)
    bap_snd =  models.CharField(max_length =100, default ="", blank = True)
    layout =  models.CharField(max_length =100, default ="", blank = True)

    #MATERIAL N OC DOCUMENT
    invoice = models.FileField(upload_to='invoice/' , blank=True, null=True)

    scopeOfWorkCount = models.IntegerField(default = 0, blank = True)
    deductionCount = models.IntegerField(default = 0, blank = True)
    paymentCount = models.IntegerField(default = 0, blank = True)
 
    def __str__(self) -> str:
        return f"{self.wo_date.strftime('%Y-%m-%d')} - {self.wo_number} - {self.category} - {self.project}"
    def wo_string(self):
        wo_date_str = self.wo_date.strftime('%Y-%m-%d') if self.wo_date else ''
        category_str = self.category if self.category else ''
        project_str = self.project if self.project else ''

        customer_str = self.customer if self.customer else ''
        type_str = self.type if self.type else ''
        cluster_name_str = self.clusterName if self.clusterName else ''
        siteid_str = self.siteId if self.siteId else ''
        odbid_str = self.odbId if self.odbId else ''
        worktype_str = self.workType if self.workType else ''

        payment_term_str = self.paymentTerm if self.paymentTerm else ''
        term_percentage_str = str(self.termPercentage) if self.termPercentage else ''

        parts = [convertDate(wo_date_str),project_str,category_str ,customer_str, type_str,cluster_name_str,siteid_str,odbid_str,worktype_str , payment_term_str, term_percentage_str]
        returnString = '-'.join(part for part in parts if part)        
        return returnString   
     
    
#date category customer type cluster siteid odbid worktype paymentterm percentage