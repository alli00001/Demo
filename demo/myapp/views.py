from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from .models import WorkOrder, ScopeOfWork, Deduction, Payment
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError
from urllib.parse import parse_qs
import re
# Create your views here.

def delete_attachment(request, id):
    if request.method == "POST":
        obj = get_object_or_404(WorkOrder, id=id)
        action = request.POST.get("action")

        # Determine which attachment to delete
        attachment_field = None
        if action == "delete_team_list":
            attachment_field = 'team_list'
        elif action == "delete_picture_of_team":
            attachment_field = 'picture_of_team'
        elif action == "delete_checklist_boq_actual_attachment":
            attachment_field = 'checklist_boq_actual_attachment'
        elif action == "delete_cover_acceptance_attachment":
            attachment_field = 'cover_acceptance_attachment'
        elif action == "delete_cover_opm":
            attachment_field = 'cover_opm_attachment'
        elif action == "delete_fac_certificate":
            attachment_field = 'fac_certificate'
        elif action == "delete_no_issue_agreement":
            attachment_field = 'no_issue_agreement'
        elif action == "delete_invoice":
            attachment_field = 'invoice'   
        elif action == "delete_capture_approval":
            attachment_field = 'capture_approval'   
        elif action == "delete_capture_drm":
            attachment_field = 'capture_drm'   
        elif action == "delete_bak":
            attachment_field = 'bak'        
        # Add additional conditions for other attachment types

        # Delete the specified attachment
        if attachment_field and hasattr(obj, attachment_field):
            attachment = getattr(obj, attachment_field)
            if attachment:
                attachment.delete()  # This deletes the file from the filesystem
                setattr(obj, attachment_field, None)  # Remove the association
                obj.save()
                return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'attachment_not_found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)
@login_required
def wo_submitted(request):
    return render(request, "wo_submitted.html")

@login_required
def home(request):
    return render(request, "home.html")
@login_required
def create_wo(request):
    context = {'MEDIA_URL': settings.MEDIA_URL}
    return render(request, "create_wo.html", context)

def mp_ln_traditional_internal_odn(request, pricing_type, company_type, project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL,'pricing_type': pricing_type, 'company_type' : company_type, 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "mp_ln_traditional_internal_odn.html", context)

        workOrder = WorkOrder(
            company = request.POST.get('company'),
            pricing_type = request.POST.get('pricing_type'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),


            clusterName = request.POST.get('clusterName'),
            odbId = request.POST.get('odbId'),
            suffixId = request.POST.get('suffixId'),
            type = request.POST.get('type'),
            workType = request.POST.get('workType'),
            hp = request.POST.get('hp'),

            grandTotalActual = request.POST.get('grand-total-actual'),
            grandTotalBoq = request.POST.get('grand-total-boq'),

            remarks1 = request.POST.get('remarks1'),
            remarks2 = request.POST.get('remarks2'),
            totalAmount = request.POST.get('grand-total-payment'),

            paymentTerm = request.POST.get('terms-selection'),
            termPercentage = request.POST.get('terms-percentage-cell'),
            termAmount = request.POST.get('terms-amount-cell'),
            termRemark = request.POST.get('payment-remarks-cell'),

            paymentTax = request.POST.get('tax-cell'),
            taxPercentage = request.POST.get('tax-percentage-cell'),
            taxAmount = request.POST.get('tax-amount-cell'),
            taxRemark = request.POST.get('tax-remarks-cell'),

            finalGrandTotal = request.POST.get('grand-total-payment2'),

            team_list = request.FILES.get('team_list'),
            picture_of_team = request.FILES.get('picture_of_team'),
            checklist_boq_actual_attachment = request.FILES.get('checklist_boq_actual_attachment'),
            cover_acceptance_attachment = request.FILES.get('cover_acceptance_attachment'),
            cover_opm_attachment = request.FILES.get('cover_opm_attachment'),
            fac_certificate = request.FILES.get('fac_certificate'),
            no_issue_agreement = request.FILES.get('no_issue_agreement'),
            invoice = request.FILES.get('invoice'),

            scopeOfWorkCount = request.POST.get('number_of_scopes'),
            deductionCount = request.POST.get('number_of_deduction'),
            paymentCount = request.POST.get('number_of_payment'),

        )
        workOrder.save()

        # CREATING SCOPE OF WORK OBJECTS
        count = request.POST.get("number_of_scopes")
        count = int(count)
        scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
        for eachScopeOfWork in scopeOfWorks :
            scopeObject = ScopeOfWork(**eachScopeOfWork)
            scopeObject.save()
            workOrder.workOrder.add(scopeObject)

        # CREATING DEDUCTION OBJECTS
            
        count2 = request.POST.get("number_of_deduction")
        count2 = int(count2)
        deductions = getDeductionInformation(request.POST, count2)
        for eachDeduction in deductions :
            deductionObject = Deduction(**eachDeduction)
            deductionObject.save()
            workOrder.deductions.add(deductionObject)

        count3 = request.POST.get("number_of_payment")
        count3 = int(count3)
        payments = getPaymentInformation(request.POST, count3)
        for eachPayment in payments :
            paymentObject = Payment(**eachPayment)
            paymentObject.save()
            workOrder.paymentInformation.add(paymentObject)
        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'mp_ln_traditional_internal_odn.html', context)

def mp_emr_traditional_internal(request, pricing_type, company_type, project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL,'pricing_type': pricing_type, 'company_type' : company_type , 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "mp_emr_traditional_internal.html", context)

        workOrder = WorkOrder(
            company = request.POST.get('company'),
            pricing_type = request.POST.get('pricing_type'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),


            clusterName = request.POST.get('clusterName'),
            siteId = request.POST.get('siteId'),
            type = request.POST.get('type'),
            workType = request.POST.get('workType'),
            hp = request.POST.get('hp'),

            grandTotalActual = request.POST.get('grand-total-actual'),
            grandTotalBoq = request.POST.get('grand-total-boq'),

            remarks1 = request.POST.get('remarks1'),
            remarks2 = request.POST.get('remarks2'),

            totalAmount = request.POST.get('grand-total-payment'),

            paymentTerm = request.POST.get('terms-selection'),
            termPercentage = request.POST.get('terms-percentage-cell'),
            termAmount = request.POST.get('terms-amount-cell'),
            termRemark = request.POST.get('payment-remarks-cell'),

            paymentTax = request.POST.get('tax-cell'),
            taxPercentage = request.POST.get('tax-percentage-cell'),
            taxAmount = request.POST.get('tax-amount-cell'),
            taxRemark = request.POST.get('tax-remarks-cell'),

            finalGrandTotal = request.POST.get('grand-total-payment2'),

            team_list = request.FILES.get('team_list'),
            picture_of_team = request.FILES.get('picture_of_team'),
            checklist_boq_actual_attachment = request.FILES.get('checklist_boq_actual_attachment'),
            cover_acceptance_attachment = request.FILES.get('cover_acceptance_attachment'),
            cover_opm_attachment = request.FILES.get('cover_opm_attachment'),
            fac_certificate = request.FILES.get('fac_certificate'),
            no_issue_agreement = request.FILES.get('no_issue_agreement'),
            invoice = request.FILES.get('invoice'),


            scopeOfWorkCount = request.POST.get('number_of_scopes'),
            deductionCount = request.POST.get('number_of_deduction'),
            paymentCount = request.POST.get('number_of_payment'),

        )
        workOrder.save()

        # CREATING SCOPE OF WORK OBJECTS
        count = request.POST.get("number_of_scopes")
        count = int(count)
        scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
        for eachScopeOfWork in scopeOfWorks :
            scopeObject = ScopeOfWork(**eachScopeOfWork)
            scopeObject.save()
            workOrder.workOrder.add(scopeObject)

        # CREATING DEDUCTION OBJECTS
            
        count2 = request.POST.get("number_of_deduction")
        count2 = int(count2)
        deductions = getDeductionInformation(request.POST, count2)
        for eachDeduction in deductions :
            deductionObject = Deduction(**eachDeduction)
            deductionObject.save()
            workOrder.deductions.add(deductionObject)
        count3 = request.POST.get("number_of_payment")
        count3 = int(count3)
        payments = getPaymentInformation(request.POST, count3)
        for eachPayment in payments :
            paymentObject = Payment(**eachPayment)
            paymentObject.save()
            workOrder.paymentInformation.add(paymentObject)

        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'mp_emr_traditional_internal.html', context)
def material_ln(request, company_type, project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL, 'company_type' : company_type , 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "material_ln.html", context)

        workOrder = WorkOrder(
            company = request.POST.get('company'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),


            clusterName = request.POST.get('clusterName'),
            suffixId = request.POST.get('suffixId'),
            odbId = request.POST.get('odbId'),

            grandTotalActual = request.POST.get('grand-total-actual'),

            remarks1 = request.POST.get('remarks1'),
            remarks2 = request.POST.get('remarks2'),
            totalAmount = request.POST.get('grand-total-payment'),

            paymentTerm = request.POST.get('terms-selection'),
            termPercentage = request.POST.get('terms-percentage-cell'),
            termAmount = request.POST.get('terms-amount-cell'),
            termRemark = request.POST.get('payment-remarks-cell'),

            paymentTax = request.POST.get('tax-cell'),
            taxPercentage = request.POST.get('tax-percentage-cell'),
            taxAmount = request.POST.get('tax-amount-cell'),
            taxRemark = request.POST.get('tax-remarks-cell'),

            finalGrandTotal = request.POST.get('grand-total-payment2'),

            invoice = request.FILES.get('invoice'),

            scopeOfWorkCount = request.POST.get('number_of_scopes'),
            deductionCount = request.POST.get('number_of_deduction'),
            paymentCount = request.POST.get('number_of_payment'),


        )
        workOrder.save()

        # CREATING SCOPE OF WORK OBJECTS
        count = request.POST.get("number_of_scopes")
        count = int(count)
        scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
        for eachScopeOfWork in scopeOfWorks :
            scopeObject = ScopeOfWork(**eachScopeOfWork)
            scopeObject.save()
            workOrder.workOrder.add(scopeObject)

        # CREATING DEDUCTION OBJECTS
            
        count2 = request.POST.get("number_of_deduction")
        count2 = int(count2)
        deductions = getDeductionInformation(request.POST, count2)
        for eachDeduction in deductions :
            deductionObject = Deduction(**eachDeduction)
            deductionObject.save()
            workOrder.deductions.add(deductionObject)

        count3 = request.POST.get("number_of_payment")
        count3 = int(count3)
        payments = getPaymentInformation(request.POST, count3)
        for eachPayment in payments :
            paymentObject = Payment(**eachPayment)
            paymentObject.save()
            workOrder.paymentInformation.add(paymentObject)


        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'material_ln.html', context)

def material_emr(request, company_type, project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL, 'company_type' : company_type, 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "material_emr.html", context)

        workOrder = WorkOrder(
            company = request.POST.get('company'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),


            clusterName = request.POST.get('clusterName'),
            siteId = request.POST.get('siteId'),

            grandTotalActual = request.POST.get('grand-total-actual'),

            remarks1 = request.POST.get('remarks1'),
            remarks2 = request.POST.get('remarks2'),
            totalAmount = request.POST.get('grand-total-payment'),

            paymentTerm = request.POST.get('terms-selection'),
            termPercentage = request.POST.get('terms-percentage-cell'),
            termAmount = request.POST.get('terms-amount-cell'),
            termRemark = request.POST.get('payment-remarks-cell'),

            paymentTax = request.POST.get('tax-cell'),
            taxPercentage = request.POST.get('tax-percentage-cell'),
            taxAmount = request.POST.get('tax-amount-cell'),
            taxRemark = request.POST.get('tax-remarks-cell'),

            finalGrandTotal = request.POST.get('grand-total-payment2'),

            invoice = request.FILES.get('invoice'),

            scopeOfWorkCount = request.POST.get('number_of_scopes'),
            deductionCount = request.POST.get('number_of_deduction'),
            paymentCount = request.POST.get('number_of_payment'),


        )
        workOrder.save()

        # CREATING SCOPE OF WORK OBJECTS
        count = request.POST.get("number_of_scopes")
        count = int(count)
        scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
        for eachScopeOfWork in scopeOfWorks :
            scopeObject = ScopeOfWork(**eachScopeOfWork)
            scopeObject.save()
            workOrder.workOrder.add(scopeObject)

        # CREATING DEDUCTION OBJECTS
            
        count2 = request.POST.get("number_of_deduction")
        count2 = int(count2)
        deductions = getDeductionInformation(request.POST, count2)
        for eachDeduction in deductions :
            deductionObject = Deduction(**eachDeduction)
            deductionObject.save()
            workOrder.deductions.add(deductionObject)

        count3 = request.POST.get("number_of_payment")
        count3 = int(count3)
        payments = getPaymentInformation(request.POST, count3)
        for eachPayment in payments :
            paymentObject = Payment(**eachPayment)
            paymentObject.save()
            workOrder.paymentInformation.add(paymentObject)

        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'material_emr.html', context)

def oc_ln(request, company_type, project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL, 'company_type' : company_type, 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "oc_ln.html", context)

        workOrder = WorkOrder(
            otherCost = request.POST.get('otherCost'),
            company = request.POST.get('company'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),

            remarks1 = request.POST.get('remarks1'),
            remarks2 = request.POST.get('remarks2'),
            clusterName = request.POST.get('clusterName'),
            suffixId = request.POST.get('suffixId'),
            odbId = request.POST.get('odbId'),

            grandTotalActual = request.POST.get('grand-total-actual'),

            totalAmount = request.POST.get('grand-total-payment'),

            paymentTerm = request.POST.get('terms-selection'),
            termPercentage = request.POST.get('terms-percentage-cell'),
            termAmount = request.POST.get('terms-amount-cell'),
            termRemark = request.POST.get('payment-remarks-cell'),

            paymentTax = request.POST.get('tax-cell'),
            taxPercentage = request.POST.get('tax-percentage-cell'),
            taxAmount = request.POST.get('tax-amount-cell'),
            taxRemark = request.POST.get('tax-remarks-cell'),

            finalGrandTotal = request.POST.get('grand-total-payment2'),

            invoice = request.FILES.get('invoice'),

            scopeOfWorkCount = request.POST.get('number_of_scopes'),
            deductionCount = request.POST.get('number_of_deduction'),
            paymentCount = request.POST.get('number_of_payment'),

        )
        workOrder.save()

        # CREATING SCOPE OF WORK OBJECTS
        count = request.POST.get("number_of_scopes")
        count = int(count)
        scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
        for eachScopeOfWork in scopeOfWorks :
            scopeObject = ScopeOfWork(**eachScopeOfWork)
            scopeObject.save()
            workOrder.workOrder.add(scopeObject)

        # CREATING DEDUCTION OBJECTS
            
        count2 = request.POST.get("number_of_deduction")
        count2 = int(count2)
        deductions = getDeductionInformation(request.POST, count2)
        for eachDeduction in deductions :
            deductionObject = Deduction(**eachDeduction)
            deductionObject.save()
            workOrder.deductions.add(deductionObject)

        count3 = request.POST.get("number_of_payment")
        count3 = int(count3)
        payments = getPaymentInformation(request.POST, count3)
        for eachPayment in payments :
            paymentObject = Payment(**eachPayment)
            paymentObject.save()
            workOrder.paymentInformation.add(paymentObject)

        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'oc_ln.html', context)

def oc_emr(request, company_type , project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL, 'company_type' : company_type, 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "oc_emr.html", context)

        workOrder = WorkOrder(
            otherCost = request.POST.get('otherCost'),
            company = request.POST.get('company'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),


            clusterName = request.POST.get('clusterName'),
            siteId = request.POST.get('siteId'),

            grandTotalActual = request.POST.get('grand-total-actual'),
            remarks1 = request.POST.get('remarks1'),
            remarks2 = request.POST.get('remarks2'),
            totalAmount = request.POST.get('grand-total-payment'),

            paymentTerm = request.POST.get('terms-selection'),
            termPercentage = request.POST.get('terms-percentage-cell'),
            termAmount = request.POST.get('terms-amount-cell'),
            termRemark = request.POST.get('payment-remarks-cell'),

            paymentTax = request.POST.get('tax-cell'),
            taxPercentage = request.POST.get('tax-percentage-cell'),
            taxAmount = request.POST.get('tax-amount-cell'),
            taxRemark = request.POST.get('tax-remarks-cell'),

            finalGrandTotal = request.POST.get('grand-total-payment2'),

            invoice = request.FILES.get('invoice'),

            scopeOfWorkCount = request.POST.get('number_of_scopes'),
            deductionCount = request.POST.get('number_of_deduction'),
            paymentCount = request.POST.get('number_of_payment'),


        )
        workOrder.save()

        # CREATING SCOPE OF WORK OBJECTS
        count = request.POST.get("number_of_scopes")
        count = int(count)
        scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
        for eachScopeOfWork in scopeOfWorks :
            scopeObject = ScopeOfWork(**eachScopeOfWork)
            scopeObject.save()
            workOrder.workOrder.add(scopeObject)

        # CREATING DEDUCTION OBJECTS
            
        count2 = request.POST.get("number_of_deduction")
        count2 = int(count2)
        deductions = getDeductionInformation(request.POST, count2)
        for eachDeduction in deductions :
            deductionObject = Deduction(**eachDeduction)
            deductionObject.save()
            workOrder.deductions.add(deductionObject)

        count3 = request.POST.get("number_of_payment")
        count3 = int(count3)
        payments = getPaymentInformation(request.POST, count3)
        for eachPayment in payments :
            paymentObject = Payment(**eachPayment)
            paymentObject.save()
            workOrder.paymentInformation.add(paymentObject)


        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'oc_emr.html', context)

def donation_ln(request, company_type , project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL, 'company_type' : company_type , 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "donation_ln.html", context)

        workOrder = WorkOrder(
            company = request.POST.get('company'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),

            clusterName = request.POST.get('clusterName'),
            odbId = request.POST.get('odbId'),
            suffixId = request.POST.get('suffixId'),

            hpD = request.POST.get('hpD'),
            unitPriceD = request.POST.get('unitPriceD'),
            amountD = request.POST.get('amountD'),
            remarkD = request.POST.get('remarkD'),

            surat_izin = request.POST.get('surat-izin'),
            bap_open = request.POST.get('bap-open'),
            capture_approval = request.FILES.get('capture_approval'),
            capture_drm = request.FILES.get('capture_drm'),
            bak = request.FILES.get('bak'),
            bap_snd = request.POST.get('bap-snd'),
            form_survey = request.POST.get('form-survey'),
            layout = request.POST.get('layout'),
        )
        workOrder.save()
        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'donation_ln.html', context)

def donation_emr(request, company_type, project_type) :
    context = {'MEDIA_URL': settings.MEDIA_URL, 'company_type' : company_type, 'project_type' : project_type}
    if request.method == "POST" :
        wo_number = request.POST.get('wo_number')
        if not wo_number:
            messages.error(request, "The work order number cannot be empty.")
            return render(request, "donation_emr.html", context)

        workOrder = WorkOrder(
            company = request.POST.get('company'),
            wo_date = request.POST.get('wo_date'),
            shortdate = request.POST.get('shortdate'),
            wo_number = request.POST.get('wo_number'),
            request_by = request.POST.get('request_by'),
            category = request.POST.get('category'),
            project = request.POST.get('project'),
            bank = request.POST.get('bank'),
            customer = request.POST.get('customer'),
            account_name = request.POST.get('account_name'),
            department = request.POST.get('department'),
            account_number = request.POST.get('account_number'),
            region = request.POST.get('region'),
            phone_number = request.POST.get('phone_number'),
            city = request.POST.get('city'),
            npwp = request.POST.get('npwp'),


            clusterName = request.POST.get('clusterName'),
            siteId = request.POST.get('siteId'),

            hpD = request.POST.get('hpD'),
            unitPriceD = request.POST.get('unitPriceD'),
            amountD = request.POST.get('amountD'),
            remarkD = request.POST.get('remarkD'),

            surat_izin = request.POST.get('surat-izin'),
            bap_open = request.POST.get('bap-open'),
            capture_approval = request.FILES.get('capture_approval'),
            capture_drm = request.FILES.get('capture_drm'),
            bak = request.FILES.get('bak'),
            bap_snd = request.POST.get('bap-snd'),
            form_survey = request.POST.get('form-survey'),
            layout = request.POST.get('layout'),
        )
        workOrder.save()
        return render(request, "wo_submitted.html", context)
    else:
    # Initial form display (GET request)
        return render(request, 'donation_emr.html', context)

def getScopeOfWorksInformation(post, count) :
    scopeOfWorks = []
    for i in range(count) :
        if (post.get(f'scopeOfWork_{i}') is not None) :
            qtyActual = safe_int_convert(post.get(f'qtyA_{i}', '0'))
            qtyBoq = safe_int_convert(post.get(f'qtyB_{i}', '0'))
            unitPrice = safe_float_convert(post.get(f'unitPrice_{i}', '0.0'))
            totalActual = safe_float_convert(post.get(f'totalA_{i}', '0.0'))
            totalBoq = safe_float_convert(post.get(f'totalB_{i}', '0.0'))

            data = {
                'scopeOfWork': post.get(f'scopeOfWork_{i}'),
                'qtyActual': qtyActual,
                'qtyBoq': qtyBoq,
                'unitPrice': unitPrice,
                'totalActual': totalActual,
                'totalBoq': totalBoq,
                'remarks': post.get(f'remarks_{i}'),
                'unit' : post.get(f'unit_{i}', default = ""),
                
            }
            scopeOfWorks.append(data)
    return scopeOfWorks

def getDeductionInformation (post,count) :
    deductionsAdditions = []
    for i in range(count) :
        if (post.get(f'deduction_{i}') is not None ):
            data = {
                'deductOrAddition'  : post.get(f'deduction_{i}'),
                'deductionAmount' : post.get(f'ded-addition-amount-cell_{i}'),
                'deductionRemarks' : post.get(f'deduction-remarks_{i}')
            }
            deductionsAdditions.append(data)
    return deductionsAdditions
def getPaymentInformation (post,count) :
    paymentInformation = []
    for i in range(count) :
        if (post.get(f'pType_{i}') is not None ):
            data = {
                'pType'  : post.get(f'pType_{i}'),
                'pPercentage' : post.get(f'pPercentage_{i}'),
                'pAmount' : post.get(f'pAmount_{i}'),
                'pStatus' : post.get(f'pStatus_{i}'),
                'pDate' : post.get(f'pDate_{i}'),
            
            }
            paymentInformation.append(data)
    return paymentInformation    

def safe_int_convert(value, default=0):
    """ Safely convert a value to an integer, using a default if conversion fails. """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float_convert(value, default=0.0):
    """ Safely convert a value to a float, using a default if conversion fails. """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

@login_required
def login_user(request):
    if request.user.is_authenticated : 
        return redirect("home")
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None :
            login(request,user)
            messages.success(request,("Welcome"))
            return redirect("home")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
@login_required
def logout_user(request) :
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect("login")
def remove_html_tags(text):
    # Use a regular expression to remove any HTML tags from the text
    clean_text = re.sub('<[^<]+?>', '', text)
    return clean_text

def normalize_string(s):
    # First, remove HTML tags, then proceed with the existing normalization steps
    s = remove_html_tags(s)
    return s.replace("–", "-").strip().lower() 
@login_required
def finished_wo(request):
    if request.method == "POST" :
        id = request.POST.get("order")
        extendable = request.POST.get("extendable") == 'on'  # This will be True if 'extendable' is 'on'        
        work_order = get_object_or_404(WorkOrder, id= id)
        if request.user.groups.filter(name='rightHand').exists():
            work_order.extendable = extendable            
            work_order.save()
                
    finished_work_orders = WorkOrder.objects.filter(
        personalAssistantCheck=True,
        ceoCheck=True,
        rightHandCheck=True,
        financeCheck=True,
    ).exclude(proofOfPayment='').order_by('-paymentDate')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        wo = request.GET.get('wo', None)
        project = request.GET.get('project', None)
        dates = request.GET.getlist('dates[]')
        category = request.GET.get('category', None)
        customer = request.GET.get('customer', None)
        region = request.GET.get('region', None)
        city = request.GET.get('city', None)
        type = request.GET.get('type', None)
        clusterName = request.GET.get('clusterName', None)
        siteId = request.GET.get('siteId', None)
        odbId = request.GET.get('odbId', None)
        suffixId = request.GET.get('suffixId', None)
        workType = request.GET.get('workType', None)
        paymentTerm = request.GET.get('paymentTerm', None)
        query = Q()
        
        if dates:
            date_queries = Q()
            for date_str in dates:
                try:
                    date_obj = parse_date(date_str)
                    if date_obj:
                        date_queries |= Q(paymentDate=date_obj)
                    else:       
                        raise ValueError(f"Invalid date format: {date_str}")
                except ValidationError:
            query &= date_queries
        if category:
            query &= Q(category__icontains=category)
        if project:
            query &= Q(project__icontains=project)
        if customer:
            query &= Q(customer__icontains=customer)
        if region:
            query &= Q(region__icontains=region)
        if city:
            query &= Q(city__icontains=city)
        if type:
            query &= Q(type__icontains=type)
        if clusterName:
            query &= Q(clusterName__icontains=clusterName)
        if siteId:
            query &= Q(siteId__icontains=siteId)
        if odbId:
            query &= Q(odbId__icontains=odbId)
        if suffixId:
            query &= Q(suffixId__icontains=suffixId)
        if type:
            query &= Q(type__icontains=type)
        if workType:
            query &= Q(workType__icontains=workType)
        if paymentTerm:
            query &= Q(paymentTerm__icontains=paymentTerm)
        finished_work_orders = finished_work_orders.filter(query).order_by('paymentDate')
        if wo:
            finished_filtered_orders = []
            for order in finished_work_orders:
                normalized_wo = normalize_string(wo.lower())
                normalized_order_string = normalize_string(order.wo_string().lower())
                if normalized_wo in normalized_order_string:
                    finished_filtered_orders.append(order)
        else:
            finished_filtered_orders = finished_work_orders.order_by('paymentDate')
        data = [
            {
                'proofOfPayment' :order.proofOfPayment.url if order.proofOfPayment else None,
                'paymentDate' : order.paymentDate,
                'project' : order.project,
                'id' : order.id,
                'wo_number': order.wo_number,
                'wo_string': order.wo_string(),
                'wo_date': order.wo_date.strftime('%Y-%m-%d') if order.wo_date else '',
                'category': order.category,
                'customer': order.customer,
                'region' : order.region,
                'company' : order.company,
                'city' : order.city,
                'type' : order.type,
                'clusterName' : order.clusterName,
                'siteId' : order.siteId,
                'odbId' : order.odbId,
                'suffixId' : order.suffixId,
                'workType' : order.workType,
                'paymentTerm' : order.paymentTerm,
                'termPercentage' : order.termPercentage,
                'finalGrandTotal' : order.finalGrandTotal,
                'url': reverse('view_wo', args=[order.wo_number, order.category, order.company, order.project]), 
                'is_rightHand': request.user.groups.filter(name='rightHand').exists(),
                'extendable' : order.extendable,
                'amountD' : order.amountD,
            }
            for order in finished_filtered_orders
        ]   
        return JsonResponse(data, safe=False)


    paginator = Paginator(finished_work_orders, 20)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    current_page = int(page_number) if page_number else 1
    starting_index = (current_page - 1) * 20

    context = {
        'page_obj': page_obj,
        'starting_index': starting_index,
        'finished': finished_work_orders,
        'is_rightHand': request.user.groups.filter(name='rightHand').exists(),
        'is_pa' :  request.user.groups.filter(name='Personal Assistant').exists(),
    }
    return render(request, 'finished_wo.html', context)
@login_required
def overview(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        # Get 'action' and 'order' from parsed data
        action = request.POST.get('action')
        orderId = request.POST.get('orderId')

        if(action == "confirm") :
            work_order = get_object_or_404(WorkOrder, id= orderId)
            if request.user.groups.filter(name__in=['CEO', 'rightHand', 'Personal Assistant', 'Finance']).exists():
                work_order.remarksOverview = request.POST.get('remarksOverview', work_order.remarksOverview)
            if request.user.groups.filter(name='CEO').exists():
                work_order.ceoCheck = request.POST.get('ceoCheck', 'false') == 'true'
            if request.user.groups.filter(name='rightHand').exists():
                work_order.rightHandCheck = request.POST.get('rightHandCheck', 'false') == 'true'
            if request.user.groups.filter(name='Personal Assistant').exists():
                work_order.personalAssistantCheck = request.POST.get('paCheck', 'false') == 'true'
                newProof = request.FILES.get('proofOfPayment')
                if newProof :
                    if work_order.proofOfPayment :
                        work_order.proofOfPayment.delete()
                    work_order.proofOfPayment = newProof
                work_order.save()
            if request.user.groups.filter(name='Finance').exists():
                work_order.financeCheck = request.POST.get('financeCheck', 'false') == 'true'
                payment_date_str = request.POST['paymentDate']
                if payment_date_str :         
                    payment_date = datetime.fromisoformat(payment_date_str)
                    work_order.paymentDate = payment_date
                else:
                    work_order.paymentDate = None 
                newProof = request.FILES.get('proofOfPayment')
                if newProof :
                    if work_order.proofOfPayment :
                        work_order.proofOfPayment.delete()
                    work_order.proofOfPayment = newProof
                work_order.save()
            due_date_str = request.POST['dueDate']
            if due_date_str :
                due_date = datetime.fromisoformat(due_date_str)
                work_order.dueDate = due_date
                work_order.save()
            else :
                work_order.dueDate = None
                work_order.save()
            return JsonResponse({'status': 'success', 'message': 'Action processed successfully'})
        elif (action == 'reject') :
            work_order = get_object_or_404(WorkOrder, id= orderId)
            if request.user.groups.filter(name__in=['CEO', 'rightHand', 'Personal Assistant', 'Finance']).exists():
                work_order.remarksOverview = request.POST.get('remarksOverview', work_order.remarksOverview)
            if request.user.groups.filter(name='CEO').exists():
                work_order.ceoReject = request.POST.get('ceoReject', 'false') == 'true'               
                work_order.save()
            if request.user.groups.filter(name='rightHand').exists():
                work_order.rightHandReject = request.POST.get('rightHandReject', 'false') == 'true'   
                work_order.save()   
            if request.user.groups.filter(name='Personal Assistant').exists():
                work_order.personalAssistantReject = request.POST.get('paReject', 'false') == 'true'     
                work_order.save()
            if request.user.groups.filter(name='Finance').exists():
                work_order.financeReject = request.POST.get('financeReject', 'false') == 'true' 
                work_order.save()
            return JsonResponse({'status': 'success', 'message': 'Action processed successfully'})
        elif (action == 'delete') :
            work_order = get_object_or_404(WorkOrder, id= orderId)
            work_order.proofOfPayment.delete()
            work_order.invoice.delete()
            work_order.team_list.delete()
            work_order.picture_of_team.delete()
            work_order.checklist_boq_actual_attachment.delete()
            work_order.cover_acceptance_attachment.delete()
            work_order.cover_opm_attachment.delete()
            work_order.fac_certificate.delete()
            work_order.no_issue_agreement.delete()
            work_order.bak.delete()
            work_order.capture_approval.delete()
            work_order.capture_drm.delete()
            work_order.delete()
            return JsonResponse({'status': 'success', 'message': 'Action processed successfully'})
    
    work_order_list = WorkOrder.objects.filter(
        Q(ceoCheck=False) |
        Q(rightHandCheck=False) |
        Q(personalAssistantCheck=False) |
        Q(financeCheck=False) |
        Q(proofOfPayment = '')
    ).order_by('-id')
    paginator = Paginator(work_order_list, 20)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    current_page = int(page_number) if page_number else 1
    starting_index = (current_page - 1) * 20

    context = {
        'page_obj': page_obj,
        'is_ceo': request.user.groups.filter(name='CEO').exists(),
        'is_rightHand': request.user.groups.filter(name='rightHand').exists(),
        'is_pa': request.user.groups.filter(name='Personal Assistant').exists(),
        'is_finance': request.user.groups.filter(name='Finance').exists(),
        'starting_index' : starting_index,
    }
    return render(request, 'overview.html', context)
@login_required
def view_wo(request, id, category, company , project):
    if (category == 'MP') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'view_wo_mp.html', context)
    if (category == 'DONATION') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'view_wo_donation.html', context)
    if (category == 'MATERIAL') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'view_wo_material.html', context)
    if (category == 'OTHER COST') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'view_wo_other_cost.html', context)

@login_required
def request_form(request, id, category, company , project):
    if (category == 'MP') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'request_form_mp.html', context)
    if (category == 'DONATION') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'request_form_donation.html', context)
    if (category == 'MATERIAL') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'request_form_material.html', context)
    if (category == 'OTHER COST') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, company = company , project = project)
        }
        return render(request, 'request_form_other_cost.html', context)

@login_required
def edit_wo(request, id, category, project):
    if (category == 'MP') :
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, category = category, project = project),        }

        if request.method == "POST" :
            wo_number = request.POST.get('wo_number')
            if not wo_number:
                messages.error(request, "The work order number cannot be empty.")
                return render(request, "edit_wo_mp.html", context)

            obj = WorkOrder.objects.get(id = id)
            # EXTEND WO CHECK
            if (obj.extendable and obj.project == 'EMR') :
                workOrder = WorkOrder(
                company = request.POST.get('company'),
                pricing_type = request.POST.get('pricing_type'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),

                clusterName = request.POST.get('clusterName'),
                siteId = request.POST.get('siteId'),
                type = request.POST.get('type'),
                workType = request.POST.get('workType'),
                hp = request.POST.get('hp'),

                grandTotalActual = request.POST.get('grand-total-actual'),
                grandTotalBoq = request.POST.get('grand-total-boq'),

                remarks1 = request.POST.get('remarks1'),
                remarks2 = request.POST.get('remarks2'),
                totalAmount = request.POST.get('grand-total-payment'),

                paymentTerm = request.POST.get('terms-selection'),
                termPercentage = request.POST.get('terms-percentage-cell'),
                termAmount = request.POST.get('terms-amount-cell'),
                termRemark = request.POST.get('payment-remarks-cell'),

                paymentTax = request.POST.get('tax-cell'),
                taxPercentage = request.POST.get('tax-percentage-cell'),
                taxAmount = request.POST.get('tax-amount-cell'),
                taxRemark = request.POST.get('tax-remarks-cell'),

                finalGrandTotal = request.POST.get('grand-total-payment2'),

                team_list = request.FILES.get('team_list'),
                picture_of_team = request.FILES.get('picture_of_team'),
                checklist_boq_actual_attachment = request.FILES.get('checklist_boq_actual_attachment'),
                cover_acceptance_attachment = request.FILES.get('cover_acceptance_attachment'),
                cover_opm_attachment = request.FILES.get('cover_opm_attachment'),
                fac_certificate = request.FILES.get('fac_certificate'),
                no_issue_agreement = request.FILES.get('no_issue_agreement'),
                invoice = request.FILES.get('invoice'),


                scopeOfWorkCount = request.POST.get('number_of_scopes'),
                deductionCount = request.POST.get('number_of_deduction'),
                paymentCount = request.POST.get('number_of_payment'),

            )
                workOrder.save()

                # CREATING SCOPE OF WORK OBJECTS
                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    workOrder.workOrder.add(scopeObject)

                # CREATING DEDUCTION OBJECTS
                    
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    workOrder.deductions.add(deductionObject)
                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    workOrder.paymentInformation.add(paymentObject)   
                return render(request, "wo_submitted.html", context)
            if (obj.extendable and obj.project == 'LN') :
                workOrder = WorkOrder(
                company = request.POST.get('company'),
                pricing_type = request.POST.get('pricing_type'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),

                clusterName = request.POST.get('clusterName'),
                odbId = request.POST.get('odbId'),
                suffixId = request.POST.get('suffixId'),
                type = request.POST.get('type'),
                workType = request.POST.get('workType'),
                hp = request.POST.get('hp'),

                grandTotalActual = request.POST.get('grand-total-actual'),
                grandTotalBoq = request.POST.get('grand-total-boq'),
                remarks1 = request.POST.get('remarks1'),
                remarks2 = request.POST.get('remarks2'),
                totalAmount = request.POST.get('grand-total-payment'),

                paymentTerm = request.POST.get('terms-selection'),
                termPercentage = request.POST.get('terms-percentage-cell'),
                termAmount = request.POST.get('terms-amount-cell'),
                termRemark = request.POST.get('payment-remarks-cell'),

                paymentTax = request.POST.get('tax-cell'),
                taxPercentage = request.POST.get('tax-percentage-cell'),
                taxAmount = request.POST.get('tax-amount-cell'),
                taxRemark = request.POST.get('tax-remarks-cell'),

                finalGrandTotal = request.POST.get('grand-total-payment2'),

                team_list = request.FILES.get('team_list'),
                picture_of_team = request.FILES.get('picture_of_team'),
                checklist_boq_actual_attachment = request.FILES.get('checklist_boq_actual_attachment'),
                cover_acceptance_attachment = request.FILES.get('cover_acceptance_attachment'),
                cover_opm_attachment = request.FILES.get('cover_opm_attachment'),
                fac_certificate = request.FILES.get('fac_certificate'),
                no_issue_agreement = request.FILES.get('no_issue_agreement'),
                invoice = request.FILES.get('invoice'),


                scopeOfWorkCount = request.POST.get('number_of_scopes'),
                deductionCount = request.POST.get('number_of_deduction'),
                paymentCount = request.POST.get('number_of_payment'),

            )
                workOrder.save()

                # CREATING SCOPE OF WORK OBJECTS
                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    workOrder.workOrder.add(scopeObject)

                # CREATING DEDUCTION OBJECTS
                    
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    workOrder.deductions.add(deductionObject)
                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    workOrder.paymentInformation.add(paymentObject)   
                return render(request, "wo_submitted.html", context)
                        
            elif (obj) :
                obj.company = request.POST.get('company')
                wo_date_str = request.POST.get('wo_date')
                obj.wo_date = parse_date(wo_date_str)
                obj.shortdate = request.POST.get('shortdate')
                obj.wo_number = request.POST.get('wo_number')
                obj.request_by = request.POST.get('request_by')
                obj.category = request.POST.get('category')
                obj.project = request.POST.get('project')
                obj.bank = request.POST.get('bank')
                obj.customer = request.POST.get('customer')
                obj.account_name = request.POST.get('account_name')
                obj.department = request.POST.get('department')
                obj.account_number = request.POST.get('account_number')
                obj.region = request.POST.get('region')
                obj.phone_number = request.POST.get('phone_number')
                obj.city = request.POST.get('city')
                obj.npwp = request.POST.get('npwp')

                if (project == 'EMR') :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.siteId = request.POST.get('siteId')
                    obj.type = request.POST.get('type')
                    obj.workType = request.POST.get('workType')
                    obj.hp = request.POST.get('hp')
                else :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.odbId = request.POST.get('odbId')
                    obj.suffixId = request.POST.get('suffixId')
                    obj.type = request.POST.get('type')
                    obj.workType = request.POST.get('workType')
                    obj.hp = request.POST.get('hp')
                    
                obj.grandTotalActual = request.POST.get('grand-total-actual')
                obj.grandTotalBoq = request.POST.get('grand-total-boq')
                obj.remarks1 = request.POST.get('remarks1')
                obj.remarks2 = request.POST.get('remarks2')
                obj.totalAmount = request.POST.get('grand-total-payment')

                obj.paymentTerm = request.POST.get('terms-selection')
                obj.termPercentage = request.POST.get('terms-percentage-cell')
                obj.termAmount = request.POST.get('terms-amount-cell')
                obj.termRemark = request.POST.get('payment-remarks-cell')

                obj.paymentTax = request.POST.get('tax-cell')
                obj.taxPercentage = request.POST.get('tax-percentage-cell')
                obj.taxAmount = request.POST.get('tax-amount-cell')
                obj.taxRemark = request.POST.get('tax-remarks-cell')

                obj.finalGrandTotal = request.POST.get('grand-total-payment2')

                new_team_list = request.FILES.get('team_list')
                if new_team_list:
                    if obj.team_list:
                        obj.team_list.delete() 
                    obj.team_list = new_team_list

                new_picture_of_team = request.FILES.get('picture_of_team')
                if new_picture_of_team:
                    if obj.picture_of_team:
                        obj.picture_of_team.delete() 
                    obj.picture_of_team = new_picture_of_team

                new_checklist_boq_actual_attachment = request.FILES.get('checklist_boq_actual_attachment')
                if new_checklist_boq_actual_attachment:
                    if obj.checklist_boq_actual_attachment:
                        obj.checklist_boq_actual_attachment.delete() 
                    obj.checklist_boq_actual_attachment = new_checklist_boq_actual_attachment
                
                new_coverAcceptance = request.FILES.get('cover_acceptance_attachment')
                if new_coverAcceptance:
                    if obj.cover_acceptance_attachment:
                        obj.cover_acceptance_attachment.delete() 
                    obj.cover_acceptance_attachment = new_coverAcceptance
                
                new_coverOpm = request.FILES.get('cover_opm_attachment')
                if new_coverOpm:
                    if obj.cover_opm_attachment:
                        obj.cover_opm_attachment.delete() 
                    obj.cover_opm_attachment = new_coverOpm    

                new_fac_certificate = request.FILES.get('fac_certificate')
                if new_fac_certificate:
                    if obj.fac_certificate:
                        obj.fac_certificate.delete() 
                    obj.fac_certificate = new_fac_certificate   

                new_no_issue_agreement = request.FILES.get('no_issue_agreement')
                if new_no_issue_agreement:
                    if obj.no_issue_agreement:
                        obj.no_issue_agreement.delete() 
                    obj.no_issue_agreement = new_no_issue_agreement  

                new_invoice = request.FILES.get('invoice')
                if new_invoice:
                    if obj.invoice:
                        obj.invoice.delete() 
                    obj.invoice = new_invoice  

                obj.scopeOfWorkCount = request.POST.get('number_of_scopes')
                obj.deductionCount = request.POST.get('number_of_deduction')
                obj.paymentCount = request.POST.get('number_of_payment')
           
                obj.save()

                for scope in obj.workOrder.all() :
                    scope.delete()

                for deduction in obj.deductions.all():
                    deduction.delete()

                for payment in obj.paymentInformation.all():
                    payment.delete()

                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    obj.workOrder.add(scopeObject)
                
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    obj.deductions.add(deductionObject)
                
                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    obj.paymentInformation.add(paymentObject)                
                return render(request, "wo_submitted.html", context)
            else :
                return render(request, "edit_wo_mp.html", context)
        return render(request, "edit_wo_mp.html", context)

    if (category == 'DONATION'):
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, category = category, project = project),        }
        if request.method == "POST" :
            wo_number = request.POST.get('wo_number')
            if not wo_number:
                messages.error(request, "The work order number cannot be empty.")
                return render(request, "edit_wo_donation.html", context)

            obj = WorkOrder.objects.get(id = id)
            if(obj.extendable and obj.project == 'LN') :
                workOrder = WorkOrder(
                company = request.POST.get('company'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),

                clusterName = request.POST.get('clusterName'),
                odbId = request.POST.get('odbId'),
                suffixId = request.POST.get('suffixId'),

                hpD = request.POST.get('hpD'),
                unitPriceD = request.POST.get('unitPriceD'),
                amount = request.POST.get('amountD'),
                remarkD = request.POST.get('remarkD'),

                surat_izin = request.POST.get('surat-izin'),
                bap_open = request.POST.get('bap-open'),
                capture_approval = request.FILES.get('capture_approval'),
                capture_drm = request.FILES.get('capture_drm'),
                bak = request.FILES.get('bak'),
                bap_snd = request.POST.get('bap-snd'),
                form_survey = request.POST.get('form-survey'),
                layout = request.POST.get('layout'),
                )
                workOrder.save()
                return render(request, "wo_submitted.html", context)
            if(obj.extendable and obj.project == 'EMR') :
                workOrder = WorkOrder(
                company = request.POST.get('company'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),

                clusterName = request.POST.get('clusterName'),
                siteId = request.POST.get('siteId'),

                hpD = request.POST.get('hpD'),
                unitPriceD = request.POST.get('unitPriceD'),
                amount = request.POST.get('amountD'),
                remarkD = request.POST.get('remarkD'),

                surat_izin = request.POST.get('surat-izin'),
                bap_open = request.POST.get('bap-open'),
                capture_approval = request.FILES.get('capture_approval'),
                capture_drm = request.FILES.get('capture_drm'),
                bak = request.FILES.get('bak'),
                bap_snd = request.POST.get('bap-snd'),
                form_survey = request.POST.get('form-survey'),
                layout = request.POST.get('layout'),
                )
                workOrder.save()
                return render(request, "wo_submitted.html", context)
            elif(obj) :
                obj.company = request.POST.get('company')
                wo_date_str = request.POST.get('wo_date')
                obj.wo_date = parse_date(wo_date_str)
                obj.shortdate = request.POST.get('shortdate')
                obj.wo_number = request.POST.get('wo_number')
                obj.request_by = request.POST.get('request_by')
                obj.category = request.POST.get('category')
                obj.project = request.POST.get('project')
                obj.bank = request.POST.get('bank')
                obj.customer = request.POST.get('customer')
                obj.account_name = request.POST.get('account_name')
                obj.department = request.POST.get('department')
                obj.account_number = request.POST.get('account_number')
                obj.region = request.POST.get('region')
                obj.phone_number = request.POST.get('phone_number')
                obj.city = request.POST.get('city')
                obj.npwp = request.POST.get('npwp')

                if (project == 'EMR') :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.siteId = request.POST.get('siteId')
                    obj.hpD = request.POST.get('hpD')
                    obj.unitPriceD = request.POST.get('unitPriceD')
                    obj.amountD = request.POST.get('amountD')
                    obj.remarkD = request.POST.get('remarkD')
                else :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.odbId = request.POST.get('odbId')
                    obj.suffixId = request.POST.get('suffixId')
                    obj.hpD = request.POST.get('hpD')
                    obj.unitPriceD = request.POST.get('unitPriceD')
                    obj.amountD = request.POST.get('amountD')
                    obj.remarkD = request.POST.get('remarkD')
                    
 

                new_capture_approval = request.FILES.get('capture_approval')
                if new_capture_approval:
                    if obj.capture_approval:
                        obj.capture_approval.delete() 
                    obj.capture_approval = new_capture_approval

                new_capture_drm = request.FILES.get('capture_drm')
                if new_capture_drm:
                    if obj.capture_drm:
                        obj.capture_drm.delete() 
                    obj.capture_drm = new_capture_drm

                new_bak = request.FILES.get('bak')
                if new_bak:
                    if obj.bak:
                        obj.bak.delete() 
                    obj.bak = new_bak

                obj.surat_izin = request.POST.get('surat-izin')
                obj.bap_open = request.POST.get('bap-open')
                obj.form_survey = request.POST.get('form-survey')
                obj.bap_snd = request.POST.get('bap-snd')
                obj.layout = request.POST.get('layout')
                obj.save()

                return render(request, "wo_submitted.html", context)
            else :
                return render(request, "edit_wo_donation.html", context)
        return render(request, "edit_wo_donation.html", context)

    if (category == 'MATERIAL'):
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, category = category, project = project),        }
        if request.method == "POST" :
            wo_number = request.POST.get('wo_number')
            if not wo_number:
                messages.error(request, "The work order number cannot be empty.")
                return render(request, "edit_wo_materials.html", context)

            obj = WorkOrder.objects.get(id = id)
            if(obj.extendable and obj.project == "EMR") :
                workOrder = WorkOrder(
                company = request.POST.get('company'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),


                clusterName = request.POST.get('clusterName'),
                siteId = request.POST.get('siteId'),

                grandTotalActual = request.POST.get('grand-total-actual'),
                remarks1 = request.POST.get('remarks1'),
                remarks2 = request.POST.get('remarks2'),
                totalAmount = request.POST.get('grand-total-payment'),

                paymentTerm = request.POST.get('terms-selection'),
                termPercentage = request.POST.get('terms-percentage-cell'),
                termAmount = request.POST.get('terms-amount-cell'),
                termRemark = request.POST.get('payment-remarks-cell'),

                paymentTax = request.POST.get('tax-cell'),
                taxPercentage = request.POST.get('tax-percentage-cell'),
                taxAmount = request.POST.get('tax-amount-cell'),
                taxRemark = request.POST.get('tax-remarks-cell'),

                finalGrandTotal = request.POST.get('grand-total-payment2'),

                invoice = request.FILES.get('invoice'),

                scopeOfWorkCount = request.POST.get('number_of_scopes'),
                deductionCount = request.POST.get('number_of_deduction'),
                paymentCount = request.POST.get('number_of_payment'),


            )
                workOrder.save()

                # CREATING SCOPE OF WORK OBJECTS
                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    workOrder.workOrder.add(scopeObject)

                # CREATING DEDUCTION OBJECTS
                    
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    workOrder.deductions.add(deductionObject)

                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    workOrder.paymentInformation.add(paymentObject)
                return render(request, "wo_submitted.html", context)
            if(obj.extendable and obj.project == "LN") :
                workOrder = WorkOrder(
                company = request.POST.get('company'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),


                clusterName = request.POST.get('clusterName'),
                suffixId = request.POST.get('suffixId'),
                odbId = request.POST.get('odbId'),

                grandTotalActual = request.POST.get('grand-total-actual'),
                remarks1 = request.POST.get('remarks1'),
                remarks2 = request.POST.get('remarks2'),
                totalAmount = request.POST.get('grand-total-payment'),

                paymentTerm = request.POST.get('terms-selection'),
                termPercentage = request.POST.get('terms-percentage-cell'),
                termAmount = request.POST.get('terms-amount-cell'),
                termRemark = request.POST.get('payment-remarks-cell'),

                paymentTax = request.POST.get('tax-cell'),
                taxPercentage = request.POST.get('tax-percentage-cell'),
                taxAmount = request.POST.get('tax-amount-cell'),
                taxRemark = request.POST.get('tax-remarks-cell'),

                finalGrandTotal = request.POST.get('grand-total-payment2'),

                invoice = request.FILES.get('invoice'),

                scopeOfWorkCount = request.POST.get('number_of_scopes'),
                deductionCount = request.POST.get('number_of_deduction'),
                paymentCount = request.POST.get('number_of_payment'),
            )
                workOrder.save()

                # CREATING SCOPE OF WORK OBJECTS
                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    workOrder.workOrder.add(scopeObject)

                # CREATING DEDUCTION OBJECTS
                    
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    workOrder.deductions.add(deductionObject)

                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    workOrder.paymentInformation.add(paymentObject)
                return render(request, "wo_submitted.html", context)

            elif(obj) :
                obj.company = request.POST.get('company')
                wo_date_str = request.POST.get('wo_date')
                obj.wo_date = parse_date(wo_date_str)
                obj.shortdate = request.POST.get('shortdate')
                obj.wo_number = request.POST.get('wo_number')
                obj.request_by = request.POST.get('request_by')
                obj.category = request.POST.get('category')
                obj.project = request.POST.get('project')
                obj.bank = request.POST.get('bank')
                obj.customer = request.POST.get('customer')
                obj.account_name = request.POST.get('account_name')
                obj.department = request.POST.get('department')
                obj.account_number = request.POST.get('account_number')
                obj.region = request.POST.get('region')
                obj.phone_number = request.POST.get('phone_number')
                obj.city = request.POST.get('city')
                obj.npwp = request.POST.get('npwp')

                if (project == 'EMR') :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.siteId = request.POST.get('siteId')
                else :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.odbId = request.POST.get('odbId')
                    obj.suffixId = request.POST.get('suffixId')
                    
                obj.grandTotalActual = request.POST.get('grand-total-actual')

                obj.totalAmount = request.POST.get('grand-total-payment')
                obj.remarks1 = request.POST.get('remarks1')
                obj.remarks2 = request.POST.get('remarks2')
                obj.paymentTerm = request.POST.get('terms-selection')
                obj.termPercentage = request.POST.get('terms-percentage-cell')
                obj.termAmount = request.POST.get('terms-amount-cell')
                obj.termRemark = request.POST.get('payment-remarks-cell')

                obj.paymentTax = request.POST.get('tax-cell')
                obj.taxPercentage = request.POST.get('tax-percentage-cell')
                obj.taxAmount = request.POST.get('tax-amount-cell')
                obj.taxRemark = request.POST.get('tax-remarks-cell')

                obj.finalGrandTotal = request.POST.get('grand-total-payment2')


                new_invoice = request.FILES.get('invoice')
                if new_invoice:
                    if obj.invoice:
                        obj.invoice.delete() 
                    obj.invoice = new_invoice

                
                obj.scopeOfWorkCount = request.POST.get('number_of_scopes')
                obj.deductionCount = request.POST.get('number_of_deduction')
                obj.paymentCount = request.POST.get('number_of_payment')

            
                obj.save()

                for scope in obj.workOrder.all() :
                    scope.delete()

                for deduction in obj.deductions.all():
                    deduction.delete()
                for payment in obj.paymentInformation.all():
                    payment.delete()
                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    obj.workOrder.add(scopeObject)
                
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    obj.deductions.add(deductionObject)
                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    obj.paymentInformation.add(paymentObject)  
                return render(request, "wo_submitted.html", context)
            else :
                return render(request, "edit_wo_materials.html", context)
        return render(request, "edit_wo_materials.html", context)
    
    if (category == 'OTHER COST') : 
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'order': get_object_or_404(WorkOrder, id=id, category = category, project = project),        }
        if request.method == "POST" :
            wo_number = request.POST.get('wo_number')
            if not wo_number:
                messages.error(request, "The work order number cannot be empty.")
                return render(request, "edit_wo_other_cost.html", context)

            obj = WorkOrder.objects.get(id = id)
            if (obj.extendable and obj.project == 'EMR') :
                workOrder = WorkOrder(
                otherCost = request.POST.get('otherCost'),
                company = request.POST.get('company'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),


                clusterName = request.POST.get('clusterName'),
                siteId = request.POST.get('siteId'),

                grandTotalActual = request.POST.get('grand-total-actual'),
                remarks1 = request.POST.get('remarks1'),
                remarks2 = request.POST.get('remarks2'),
                totalAmount = request.POST.get('grand-total-payment'),

                paymentTerm = request.POST.get('terms-selection'),
                termPercentage = request.POST.get('terms-percentage-cell'),
                termAmount = request.POST.get('terms-amount-cell'),
                termRemark = request.POST.get('payment-remarks-cell'),

                paymentTax = request.POST.get('tax-cell'),
                taxPercentage = request.POST.get('tax-percentage-cell'),
                taxAmount = request.POST.get('tax-amount-cell'),
                taxRemark = request.POST.get('tax-remarks-cell'),

                finalGrandTotal = request.POST.get('grand-total-payment2'),

                invoice = request.FILES.get('invoice'),

                scopeOfWorkCount = request.POST.get('number_of_scopes'),
                deductionCount = request.POST.get('number_of_deduction'),
                paymentCount = request.POST.get('number_of_payment'),


            )
                workOrder.save()

                # CREATING SCOPE OF WORK OBJECTS
                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    workOrder.workOrder.add(scopeObject)

                # CREATING DEDUCTION OBJECTS
                    
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    workOrder.deductions.add(deductionObject)

                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    workOrder.paymentInformation.add(paymentObject)     
                return render(request, "wo_submitted.html", context)
            if (obj.extendable and obj.project == 'LN') :
                workOrder = WorkOrder(
                otherCost = request.POST.get('otherCost'),
                company = request.POST.get('company'),
                wo_date = request.POST.get('wo_date'),
                shortdate = request.POST.get('shortdate'),
                wo_number = request.POST.get('wo_number'),
                request_by = request.POST.get('request_by'),
                category = request.POST.get('category'),
                project = request.POST.get('project'),
                bank = request.POST.get('bank'),
                customer = request.POST.get('customer'),
                account_name = request.POST.get('account_name'),
                department = request.POST.get('department'),
                account_number = request.POST.get('account_number'),
                region = request.POST.get('region'),
                phone_number = request.POST.get('phone_number'),
                city = request.POST.get('city'),
                npwp = request.POST.get('npwp'),


                clusterName = request.POST.get('clusterName'),
                odbId = request.POST.get('odbId'),
                suffixId = request.POST.get('suffixId'),

                grandTotalActual = request.POST.get('grand-total-actual'),
                remarks1 = request.POST.get('remarks1'),
                remarks2 = request.POST.get('remarks2'),
                totalAmount = request.POST.get('grand-total-payment'),

                paymentTerm = request.POST.get('terms-selection'),
                termPercentage = request.POST.get('terms-percentage-cell'),
                termAmount = request.POST.get('terms-amount-cell'),
                termRemark = request.POST.get('payment-remarks-cell'),

                paymentTax = request.POST.get('tax-cell'),
                taxPercentage = request.POST.get('tax-percentage-cell'),
                taxAmount = request.POST.get('tax-amount-cell'),
                taxRemark = request.POST.get('tax-remarks-cell'),

                finalGrandTotal = request.POST.get('grand-total-payment2'),

                invoice = request.FILES.get('invoice'),

                scopeOfWorkCount = request.POST.get('number_of_scopes'),
                deductionCount = request.POST.get('number_of_deduction'),
                paymentCount = request.POST.get('number_of_payment'),
            )
                workOrder.save()

                # CREATING SCOPE OF WORK OBJECTS
                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    workOrder.workOrder.add(scopeObject)

                # CREATING DEDUCTION OBJECTS
                    
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    workOrder.deductions.add(deductionObject)

                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    workOrder.paymentInformation.add(paymentObject)     
                return render(request, "wo_submitted.html", context)
            elif(obj) :
                obj.otherCost = request.POST.get('otherCost')
                obj.company = request.POST.get('company')
                wo_date_str = request.POST.get('wo_date')
                obj.wo_date = parse_date(wo_date_str)
                obj.shortdate = request.POST.get('shortdate')
                obj.wo_number = request.POST.get('wo_number')
                obj.request_by = request.POST.get('request_by')
                obj.category = request.POST.get('category')
                obj.project = request.POST.get('project')
                obj.bank = request.POST.get('bank')
                obj.customer = request.POST.get('customer')
                obj.account_name = request.POST.get('account_name')
                obj.department = request.POST.get('department')
                obj.account_number = request.POST.get('account_number')
                obj.region = request.POST.get('region')
                obj.phone_number = request.POST.get('phone_number')
                obj.city = request.POST.get('city')
                obj.npwp = request.POST.get('npwp')

                if (project == 'EMR') :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.siteId = request.POST.get('siteId')
                else :
                    obj.clusterName = request.POST.get('clusterName')
                    obj.odbId = request.POST.get('odbId')
                    obj.suffixId = request.POST.get('suffixId')
                    
                obj.grandTotalActual = request.POST.get('grand-total-actual')
                obj.remarks1 = request.POST.get('remarks1')
                obj.remarks2 = request.POST.get('remarks2')
                obj.totalAmount = request.POST.get('grand-total-payment')

                obj.paymentTerm = request.POST.get('terms-selection')
                obj.termPercentage = request.POST.get('terms-percentage-cell')
                obj.termAmount = request.POST.get('terms-amount-cell')
                obj.termRemark = request.POST.get('payment-remarks-cell')

                obj.paymentTax = request.POST.get('tax-cell')
                obj.taxPercentage = request.POST.get('tax-percentage-cell')
                obj.taxAmount = request.POST.get('tax-amount-cell')
                obj.taxRemark = request.POST.get('tax-remarks-cell')

                obj.finalGrandTotal = request.POST.get('grand-total-payment2')


                new_invoice = request.FILES.get('invoice')
                if new_invoice:
                    if obj.invoice:
                        obj.invoice.delete() 
                    obj.invoice = new_invoice

                
                obj.scopeOfWorkCount = request.POST.get('number_of_scopes')
                obj.deductionCount = request.POST.get('number_of_deduction')
                obj.paymentCount = request.POST.get('number_of_payment')
           
                obj.save()

                for scope in obj.workOrder.all() :
                    scope.delete()

                for deduction in obj.deductions.all():
                    deduction.delete()

                for payment in obj.paymentInformation.all():
                    payment.delete()

                count = request.POST.get("number_of_scopes")
                count = int(count)
                scopeOfWorks = getScopeOfWorksInformation(request.POST, count)
                for eachScopeOfWork in scopeOfWorks :
                    scopeObject = ScopeOfWork(**eachScopeOfWork)
                    scopeObject.save()
                    obj.workOrder.add(scopeObject)
                
                count2 = request.POST.get("number_of_deduction")
                count2 = int(count2)
                deductions = getDeductionInformation(request.POST, count2)
                for eachDeduction in deductions :
                    deductionObject = Deduction(**eachDeduction)
                    deductionObject.save()
                    obj.deductions.add(deductionObject)
                count3 = request.POST.get("number_of_payment")
                count3 = int(count3)
                payments = getPaymentInformation(request.POST, count3)
                for eachPayment in payments :
                    paymentObject = Payment(**eachPayment)
                    paymentObject.save()
                    obj.paymentInformation.add(paymentObject)  
                return render(request, "wo_submitted.html", context)
            else :
                return render(request, "edit_wo_oc.html", context)
            
        return render(request, "edit_wo_oc.html", context)

def delete_wo(request, id):
    targetWO = WorkOrder(get_object_or_404, id = id)
    targetWO.delete()
    return redirect('wo_submitted')