# -*- coding: utf-8 -*-
"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import requests
import string
import sys

import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse

from opaque_keys.edx.keys import CourseKey, UsageKey
from lms.djangoapps.courseware.courses import get_course_by_id, get_course_with_access
from openedx.core.djangoapps.course_groups.cohorts import is_course_cohorted
from lms.djangoapps.instructor_analytics.basic import enrolled_students_features
import lms.djangoapps.instructor_analytics.csvs
import lms.djangoapps.instructor_analytics.distributions
from django.conf import settings as DJANGO_SETTINGS

from django.contrib.auth.models import User

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean, Dict, Float, List, Set, Field, ScopeIds
from xblock.fragment import Fragment

from django.utils.translation import ugettext as _
from django.template import Context, Template
from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
from .utils import render_template, xblock_field_list

from mock import patch, MagicMock, Mock
from xblock.field_data import FieldData, DictFieldData
from xblock.runtime import Runtime

import logging
log = logging.getLogger(__name__)


class SmowlCheckRegXblock(XBlock):
    """
    XBlock displaying an iframe, with an anonymous ID passed in argument
    """

    # Fields are defined on the class. You can access them in your code as
    # self.<fieldname>.

    # URL format :
    # {iframe_url}/UserID

    nombresAlum = ""
    entidadEDX = ""

    display_name = String(
        help=_("SMOWL"),
        display_name=_("Component Display Name"),
        # name that appears in advanced settings studio menu
        default=_("SMOWL CHECK REGISTER"),
        scope=Scope.user_state
    )

    smowlcheckreg_url = String(
        display_name=_("SMOWL ACTIVATED"),
        help=_("PUBLISH to activate SMOWL"),
        default="",
        scope=Scope.settings
    )

    has_author_view = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")
    
    def author_view(self, context=None):
        lms_base = SiteConfiguration.get_value_for_org(
            self.location.org,
            "LMS_BASE",
            DJANGO_SETTINGS.LMS_BASE
        )
        context = {
            'has_settings': self.check_settings(),
            'help_url': 'https://{}/{}'.format(lms_base, 'contact_form')
        }
        frag = Fragment()
        frag.add_content(render_template(
            '/templates/html/smowlcheckreg-author.html', context))
        frag.add_css(self.resource_string("static/css/smowlcheckreg.css"))
        frag.initialize_js('SmowlCheckRegXblock')
        return frag

    def student_view(self, context=None):
        """
        The primary view of the SMOWLCHECKREGISTER, shown to students
        when viewing courses.
        """

        #runtime = TestRuntime(services={'field-data': DictFieldData({})})
        #block = SmowlCheckRegXblock(runtime, scope_ids=Mock(spec=ScopeIds))
        #parent = block.get_parent()

        #url_response = self.request.GET

        # student es la id del curso y sirve pa saber si es admin
        user_id = self.scope_ids.user_id

        course_id = self.xmodule_runtime.course_id
        #usageID =  self.scope_ids.usage_id

        # usage es el codigo del curso mejor asi
        #usage5555 = self.scope_ids.usage_id

        idUnit2 = self.parent
        idUnit = str(idUnit2).split("@")[-1]
        #idUnit5 = "{0}".format(idUnit)

        idCurso = self.course_id
        # Para poder sacar todos los nombres y ids
        course = self.course_id

        query_features = [
            'id', 'name',
        ]
        settings = {
            'has_settings': False
        }
        if self.check_settings():
            student_data = enrolled_students_features(
                course, query_features)

            #ikasleak2 = student_data[1]['name']
            ikasleak = student_data

            tamEnrolados = len(student_data)
            listaEnrolados = ""

            for i in range(tamEnrolados):
                listaEnrolados += "," + \
                    student_data[i]['id']+"."+student_data[i]['name']

            listaEnrolados = listaEnrolados.replace(" ", "_")
            listaEnrolados = listaEnrolados.replace(",", "", 1)

            listaEnrolados = listaEnrolados.encode('utf-8', 'ignore')
            entityName = DJANGO_SETTINGS.SMOWL_ENTITY
            entityName = entityName.encode('utf-8')

            new_smowlcheckreg_url = "hola {0} ADDDDDDDDDDDDDDDDDDDDD {1} ".format(
                entityName, listaEnrolados)

            # QUITAR para probar
            #self.display_name = new_smowlcheckreg_url

            context = {
                'self': self,
                'location': str(self.location).split('@')[-1],
                'smowlcheckreg_url': new_smowlcheckreg_url,
                'entity_Name': DJANGO_SETTINGS.SMOWL_ENTITY,
                'nombresAlum': listaEnrolados,
                'entidadEDX': entityName,
                'swlLicenseKey': DJANGO_SETTINGS.SMOWL_KEY,
                'SMOWLCHECKREG_URL': DJANGO_SETTINGS.SMOWLCHECKREG_URL,
                'has_settings': True
            }
            settings['has_settings'] = True
        else:
            context = {
                'has_settings': False
            }
        frag = Fragment()
        frag.add_content(render_template(
            '/templates/html/smowlcheckreg.html', context))
        frag.add_css(self.resource_string("static/css/smowlcheckreg.css"))
        frag.add_javascript(self.resource_string(
            "static/js/src/smowlcheckreg.js"))
        frag.initialize_js('SmowlCheckRegXblock', json_args=settings)
        return frag

    def studio_view(self, context=None):
        """
        The studio view of the SMOWLCHECKREGISTER, with form
        """
        frag = Fragment()
        frag.add_content(render_template(
            '/templates/html/smowlcheckreg-edit.html'))
        frag.add_javascript(self.resource_string(
            "static/js/src/smowlcheckreg-edit.js"))
        frag.initialize_js('SmowlCheckRegXblock')
        return frag

    def check_settings(self):
        return (
            hasattr(DJANGO_SETTINGS, 'SMOWLCHECKREG_URL') and 
            hasattr(DJANGO_SETTINGS, 'SMOWL_KEY') and 
            hasattr(DJANGO_SETTINGS, 'SMOWL_ENTITY')
            )

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SmowlCheckRegXblock",
             """
			 """),
        ]
