from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from users.forms import SignupForm, LoginForm
from utils.email import send_verification_email  # 이건 utils/email.py 에 작성 예정

User = get_user_model()
signer = TimestampSigner()

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # 인증 전까진 비활성화
        user.save()

        # 이메일 인증 메일 발송
        send_verification_email(self.request, user)

        return render(self.request, 'registration/signup_done.html', {'email': user.email})

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('cbv_todo_list')
            else:
                form.add_error(None, '이메일 인증이 필요합니다.')
        else:
            form.add_error(None, '이메일 또는 비밀번호가 올바르지 않습니다.')

        return self.form_invalid(form)

def verify_email(request):
    code = request.GET.get("code")
    try:
        email = signer.unsign(code, max_age=60 * 60 * 24)  # 24시간 유효
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return render(request, "registration/verify_success.html")

    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return render(request, "registration/verify_failed.html")
