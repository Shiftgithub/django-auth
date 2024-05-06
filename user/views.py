import secrets
from .form import *
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_info_form = UserInfoForm(request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            token_str = generate_token(6)
            user = user_form.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            otp_form = VerifyOtp(otp=token_str, user=user_info.user)
            otp_form.save()
            user_info.save()

            user_id = user.id
            request.session['temp_verify_id'] = user_id
            email = user.email
            request.session['temp_verify_email'] = email

            return redirect('otp_setup')  # You should have a URL named 'otp_setup'
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    context = {'user_form': user_form, 'user_info_form': user_info_form}
    return render(request, 'registration.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True
                user.save()
                # Log the user in
                auth_login(request, user)
            return redirect('dashboard')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('login')


def dashboard(request):
    return render(request, 'dashboard.html')


def generate_token(length):
    return str(secrets.randbelow(10 ** 6)).zfill(length)


def verify_otp(request):
    if request.method == 'POST':
        otp_form = VerifyOtpForm(request.POST)
        user_id = request.session.get('temp_verify_id')

        if otp_form.is_valid():
            otp = otp_form.cleaned_data['otp']

            try:
                otp_entry = VerifyOtp.objects.get(otp=otp, user__id=user_id)
            except VerifyOtp.DoesNotExist:
                # Handle OTP not found or doesn't match the user
                return render(request, 'enter_otp.html', {'otp_form': otp_form})

            # OTP found and matched, mark it as verified
            otp_entry.is_verified = True
            otp_entry.otp = 0
            otp_entry.save()

            # Activate the user's account by setting is_active to True
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            # Update UserInfo status to 'active'
            try:
                user_info = UserInfo.objects.get(user=user)
                user_info.status = 'active'
                user_info.save()
            except UserInfo.DoesNotExist:
                # Handle UserInfo not found
                pass  # You can log or handle this case accordingly

            return redirect('login')  # Redirect to success page
        else:
            print('Error')

    else:
        otp_form = VerifyOtpForm()

    context = {'otp_form': otp_form}
    return render(request, 'enter_otp.html', context)
