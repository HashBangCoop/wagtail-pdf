from datetime import datetime

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel#, InlinePanel, MultiFieldPanel, FieldRowPanel

from wagtail_pdf_view.mixins import PdfViewPageMixin, PdfModelMixin

# TODO reenable
#from wagtail_pdf_view.views import WagtailTexView


from django.conf import settings


class DemoModel(PdfModelMixin, models.Model):
    creation_date = models.DateField(default=datetime.now)
    
    author = models.CharField(max_length=200)
    
    content = StreamField([
        ("heading", blocks.CharBlock(form_classname="full title")),
        ("text", blocks.RichTextBlock()),
    ], blank=True)
    
    panels = [
        FieldPanel("creation_date"),
        FieldPanel("author"),
        StreamFieldPanel("content"),
    ]
    
    template_name = "home/demo_model.html"
    
    # Alternative: Override the get_template() method
    # def get_template(self, request, *args, extension=None, **kwargs):
    #     return "home/demo_model.html"
    


class SimplePdfPage(PdfViewPageMixin, Page):
    ## Set the browsers attachment handling
    # attachment = True
    
    ## render with LaTeX instead
    # PDF_VIEW_PROVIDER = WagtailTexView
    
    ## Add a custom view provider or method
    #def get_pdf_view(self):
    #    return WagtailTexView(self).serve
    
    creation_date = models.DateField(default=datetime.now)
    
    author = models.CharField(max_length=200)
    
    content = StreamField([
        ("heading", blocks.CharBlock(form_classname="full title")),
        ("text", blocks.RichTextBlock()),
    ], blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel("creation_date"),
        FieldPanel("author"),
        StreamFieldPanel("content"),
    ]
    
    
    # stylesheets = [settings.STATIC_ROOT + "/css/demo_page.css"]
    stylesheets = ["css/demo_page.css"]

    #def get_stylesheets(self, request):
    #    return ["css/demo_page.css"]

from wagtail.core.fields import RichTextField

from wagtail.images.blocks import ImageChooserBlock
    
class HtmlAndPdfPage(PdfViewPageMixin, Page):
    
    # Set the browsers attachment handling
    attachment = models.BooleanField(help_text="Download the .pdf file instead of displaying it in the browser", default=False)
    
    ## PDF first
    # ROUTE_CONFIG = [
    #     ("pdf", r'^$'),
    #     ("html", r'^html/$'),
    # ]
    
    # HTML first
    ROUTE_CONFIG = [
        ("pdf", r'^pdf/$'),
        ("html", r'^$'),
    ]
    
    ## You can rename the default preview modes
    # preview_modes = [
    #    ("pdf", "My Pdf Preview"),
    #    ("html", "My HTML Preview"),
    # ]
    
    creation_date = models.DateField(default=datetime.now)
    
    author = models.CharField(max_length=200)
    
    address = models.TextField(blank=True)
    
    content = StreamField([
        ("heading", blocks.CharBlock(form_classname="full title")),
        ("text", blocks.RichTextBlock()),
        ("image", ImageChooserBlock())
        
    ], blank=True)
    
    
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel("creation_date"),
        FieldPanel("author"),
        FieldPanel("address"),
        FieldPanel("body"),
        StreamFieldPanel("content"),
    ]
    
    
    
    pdf_base_template = "pdf_document_base.html"
    
    def get_stylesheets(self, request, mode=None, **kwargs):
        
        # TODO default stylesheets
        # SCSS --> CSS (and remove leading '/')
        return []# return [sass_processor('scss/style_document.pdf.scss')[1:] ]
    
    def get_context(self, request, mode=None, **kwargs):
        context = super().get_context(request, **kwargs)
        
        if mode == 'pdf':
            context["override_base"] = self.pdf_base_template
        
        return context
    
