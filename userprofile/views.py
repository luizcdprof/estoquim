import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

# superuser - admin - t3st3s3c

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

@csrf_exempt
def userprofile_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            if user is not None:
                login(request, user)  # <--- ESSENCIAL: Isso cria a sessão e prepara o cookie
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def userprofile_view(request):
    if request.method == 'POST':
        usuario = request.user
        # Resposta para requisição AJAX (JSON)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            profile = UserProfile.objects.filter(user=usuario).first()
            usuario_data = {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'birthdate': profile.birthdate.isoformat() if profile and profile.birthdate else None,
            }
            return JsonResponse({'success': True, 'usuario': usuario_data})

    return JsonResponse(
        {
            'erro': 'Método não permitido'
        }, status=405
    )

@login_required
@csrf_exempt
def userprofile_list(request):
    if request.method == 'POST':
        usuario = request.user
        if usuario.is_staff:  # Apenas usuários com permissão de staff podem acessar a lista completa
            usuarios = UserProfile.objects.all()
            usuarios_data = []

            # Resposta para requisição AJAX (JSON)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Converte o objeto de usuário em um dicionário para serializar
                for usuario in usuarios:
                    usuarios_data.append({
                        'id': usuario.id,
                        'username': usuario.user.username,
                        'email': usuario.user.email,
                        'birthdate': usuario.birthdate
                    })
                return JsonResponse({'success': True, 'usuarios': usuarios_data})
        else:
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)

    return JsonResponse(
        {
            'erro': 'Método não permitido'
        }, status=405
    )

@login_required
@csrf_exempt
def userprofile_register(request):
    if request.method == 'POST':
        # 1. Transforma o JSON do Bruno em um dicionário python
        data = json.loads(request.body)

        # 2. Cria o User padrão do Django (criptografando a senha)
        new_user = User.objects.create_user(
            username = data['username'],
            password = data['password'],
            email = data['email']
        )

        # 3. Cria o UserProfile vinculando ao User criado acima
        new_user_profile = UserProfile.objects.create(
            user = new_user,
            birthdate = data['birthdate']
        )

        return JsonResponse(
            {
                'status': 'Sucesso',
                'message': 'Usuário criado!',
            }, status=201
        )
    return JsonResponse(
        {
            'erro': 'Método não permitido'
        }, status=405
    )
