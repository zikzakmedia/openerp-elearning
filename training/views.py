# -*- encoding: utf-8 -*-
############################################################################################
#
#    OpenERP e-learning, Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

from settings import *
from tools.conn import conn_webservice
from tools.elearning import checkContactID, checkFullName, connOOOP

from wiki import wiki2html

@login_required
def index(request):
    """Training Index page"""
    contact_id = checkContactID(request)
    if not contact_id:
        error = _('Are you a student? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    conn = connOOOP()
    if not conn:
        error = _('Error when you are connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    full_name = checkFullName(request)
    contact = conn.ResPartnerContact.get(contact_id)

    offers = contact.offer_ids
    site_title = SITE_TITLE

    title = _('My offers :: %(full_name)s') % {'full_name':full_name}
    metadescription = _('Offers Frontpage of %(full_name)s') % {'full_name':full_name}

    return render_to_response("training/index.html", locals(), context_instance=RequestContext(request))

@login_required
def offer(request, offer):
    """Training Offer page"""
    contact_id = checkContactID(request)
    if not contact_id:
        error = _('Are you a student? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    conn = connOOOP()
    if not conn:
        error = _('Error when you are connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    full_name = checkFullName(request)
    contact = conn.ResPartnerContact.get(contact_id)

    offer = conn.TrainingOffer.filter(alias=offer)
    if len(offer) == 0:
        error = _('The page requested could not be found.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    check_offer = False
    contact_offers = contact.offer_ids
    for contact_offer in contact_offers:
        if contact_offer.id == offer[0].id:
            check_offer = True

    if check_offer:
        offer = offer[0]
        title = offer.name
        site_title = SITE_TITLE

        metadescription = offer.metadescription
        metakeywords = offer.metakey and offer.metakey or ''
        url = LIVE_URL

        courses = []
        for course in offer.course_ids:
            course = conn.TrainingCourse.get(course.course_id.id)
            courses.append({'name':course.long_name, 'alias':course.alias, 'wikis': course.course_wiki_pages_ids, 'course': course})

        return render_to_response("training/offer.html", locals(), context_instance=RequestContext(request))
    else:
        error = _('The page requested  could not be found.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

@login_required
def wiki(request, offer, wiki):
    """Training Offer page"""
    contact_id = checkContactID(request)
    if not contact_id:
        error = _('Are you a student? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    conn = connOOOP()
    if not conn:
        error = _('Error when you are connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    full_name = checkFullName(request)
    contact = conn.ResPartnerContact.get(contact_id)

    #TODO: check if have rules access view this source
    offer = conn.TrainingOffer.filter(alias=offer)
    if len(offer) == 0:
        error = _('The page requested could not be found.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    wiki = conn.WikiWiki.filter(alias=wiki)
    if len(wiki) == 0:
        error = _('The page requested could not be found.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    wiki = wiki[0]
    offer = offer[0]
    
    if wiki.text_area:
        wiki_content = wiki2html(wiki.text_area, True, wiki.id)
        wiki_content = wiki_content.replace('[offer]',offer.alias) #replace tag [offer] for alias offer
    else:
        wiki_content = _('There are not any content available')

    url = LIVE_URL
    title = wiki.name
    site_title = SITE_TITLE
    metadescription = _('%(title)s wiki') % {'title': wiki.name}
    metakeywords = wiki.tags or ''

    courses = []
    for course in offer.course_ids:
        course = conn.TrainingCourse.get(course.course_id.id)
        courses.append({'name':course.long_name, 'alias':course.alias, 'wikis': course.course_wiki_pages_ids})

    return render_to_response("training/wiki.html", locals(), context_instance=RequestContext(request))

@login_required
def exam(request, offer, course, exam):
    """Training Exam/Questionarie page
    """
    contact_id = checkContactID(request)
    if not contact_id:
        error = _('Are you a student? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    conn = connOOOP()
    if not conn:
        error = _('Error when you are connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    full_name = checkFullName(request)
    contact = conn.ResPartnerContact.get(contact_id)

    #TODO: check if have rules access view this source
    offer = conn.TrainingOffer.filter(alias=offer)
    if len(offer) == 0:
        error = _('The page requested could not be found.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    course = conn.TrainingCourse.filter(alias=course)
    if len(course) == 0:
        error = _('The page requested could not be found.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    exam = conn.TrainingExamQuestionnaire.filter(alias=exam)
    if len(exam) == 0:
        error = _('The page requested could not be found.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    offer = offer[0]
    course = course[0]
    exam = exam[0]

    #check if contact make this exam
    make_exam = True
    for part in conn.TrainingParticipation.filter(contact_id=contact_id):
        if course.id == part.seance_id.course_id.id:
            participation = part
            if part.questionnaire_id:
                make_exam = False

    url = LIVE_URL
    title = exam.name
    site_title = SITE_TITLE
    metadescription = exam.metadescription or _('Questionaire %(name)s') % {'name':exam.name}
    metakeywords = exam.metakey or ''

    path_info = request.path_info.split('/')

    if 'questionarie' in path_info: #questionaire page
        #list questions
        questions_questions = conn.TrainingExamQuestionnaireQuestion.filter(questionnaire_id=exam.id)
        questions = []
        for question in questions_questions:
            questions.append(question.question_id)

        return render_to_response("training/questionarie.html", locals(), context_instance=RequestContext(request))

    if 'answer' in path_info: #questionaire page
        if request.method == 'POST':
            values = request.POST
            if len(values) > 0:
                #add participation questionaire
                participation.questionnaire_id = exam
                participation.result_received = True
                participation.save()
                make_exam = False

                #reload participation
                participation_id = participation.id
                del participation

            i = 1
            for k, v in values.iteritems():
                answer_values = {}
                value = k.split('_')
                if len(value) > 1:
                    answer_values['participation_id'] = participation_id
                    if value[1][-2:] == '[]':
                        answer_values['question_id'] = value[1][:-2]
                    else:
                        answer_values['question_id'] = value[1]
                    if value[0] == 'qcm':
                        answer_values['response_qcm_ids'] = [v]
                    if value[0] == 'qcu':
                        answer_values['response_qcu_ids'] = [v]
                    if value[0] == 'yesno':
                        answer_values['response_yesno'] = v
                    if value[0] == 'plain':
                        answer_values['response_plain'] = v
                    answer_values['sequence'] = i
                    i = i+1

                    # create participation line questions
                    answer_exam = conn_webservice('training.participation.line','question_answer', [answer_values])

            participation = conn.TrainingParticipation.get(participation_id) #reload participation

    return render_to_response("training/exam.html", locals(), context_instance=RequestContext(request))
