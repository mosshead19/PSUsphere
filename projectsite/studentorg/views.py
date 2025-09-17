from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from studentorg.models import Organization
from studentorg.forms import OrganizationForm
from django.urls import reverse_lazy

from studentorg.models import OrgMember, Student, College, Program

from django.db.models import Q
from django.utils import timezone

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()
        context["total_programs"] = Program.objects.count()
        context["total_organizations"] = Organization.objects.count()

        today = timezone.now().date()
        count = (
            OrgMember.objects.filter(
                date_joined__year=today.year
            )
            .values("student")
            .distinct()
            .count()
        )

        context["students_joined_this_year"] = count
        return context


class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5
    ordering = ["college__college_name","name"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
            Q(name__icontains=query) 
        |   Q(description__icontains=query) 
        |   Q(college__college_name__icontains=query)
    )
        return qs


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')
class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')


class OrgMemberListView(ListView):
    model = OrgMember
    context_object_name = 'orgmembers'
    template_name = 'orgmember_list.html'
    paginate_by = 5

    def get_ordering(self):
        allowed = ["student__lastname", "student__firstname", "date_joined"]
        sort_by = self.request.GET.get("sort_by", "student__lastname")
        sort_order = self.request.GET.get("sort_order", "asc")
        if sort_by not in allowed:
            sort_by = "student__lastname"
        if sort_by == "student__lastname":
            ordering = ["student__lastname", "student__firstname"]
        else:
            ordering = [sort_by]
        if sort_order == "desc":
            ordering = ["-" + field for field in ordering]
        return ordering
        
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(student__lastname__icontains=q) 
            |   Q(student__firstname__icontains=q) 
            |   Q(date_joined__year__icontains=q) 
            |   Q(date_joined__month__icontains=q) 
            |   Q(date_joined__day__icontains=q) 
            |   Q(organization__name__icontains=q) 
        )
            
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    fields = '__all__'
    template_name = 'orgmember_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    fields = '__all__'
    template_name = 'orgmember_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')

# Student Views
class StudentListView(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(lastname__icontains=q)
            |   Q(firstname__icontains=q)
            |   Q(middlename__icontains=q) 
            |   Q(student_id__icontains=q)
            |   Q(program__prog_name__icontains=q)
        )
        return qs

class StudentCreateView(CreateView):
    model = Student
    fields = '__all__'
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    fields = '__all__'
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')

# College Views
class CollegeListView(ListView):
    model = College
    context_object_name = 'colleges'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(college_name__icontains=q)
        return qs

class CollegeCreateView(CreateView):
    model = College
    fields = '__all__'
    template_name = 'college_form.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    fields = '__all__'
    template_name = 'college_form.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

# Program Views
class ProgramListView(ListView):
    model = Program
    context_object_name = 'programs'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_ordering(self):
        allowed = ["prog_name", "college__college_name"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "prog_name"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(prog_name__icontains=q)
            | Q(college__college_name__icontains=q)
        )
            

        return qs

class ProgramCreateView(CreateView):
    model = Program
    fields = '__all__'
    template_name = 'program_form.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    fields = '__all__'
    template_name = 'program_form.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')


