from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Comment, SearchLog
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login

# ---------- VULNERABLE LOGIN (auth bypass + error-based) ----------
def vuln_login(request):
    msg = None
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        # VULN: string-concatenated credentials
        q = f"SELECT id, username FROM auth_user WHERE username='{u}' AND password='{p}'"
        try:
            with connection.cursor() as cur:
                cur.execute(q)
                row = cur.fetchone()
        except Exception as e:
            # VULN: raw DB error leaks SQL and version to the client
            return HttpResponse(f"<h3>Database error (debug leak):</h3><pre>{e}</pre>", status=500)
        if row:
            # Establish a real Django session (logged in as the matched user)
            user = User.objects.get(id=row[0])
            django_login(request, user)
            request.session['vuln_user'] = row[1]
            return render(request, 'shop/profile.html',{'username': row[1], 'via': 'vuln-login'})
        msg = 'Invalid credentials'
    return render(request, 'shop/login.html', {'msg': msg})

# ---------- VULNERABLE SEARCH (classic injection point) ----------
def vuln_search(request):
    q = request.GET.get('q', '')
    if q:
        SearchLog.objects.create(query=q, user=request.user if request.user.is_authenticated else None)
        # VULN: direct concatenation into WHERE clause
        sql = f"SELECT id, name, price, category FROM shop_product WHERE name LIKE '%{q}%' OR description LIKE '%{q}%'"
        try:
            with connection.cursor() as cur:
                cur.execute(sql)
                results = [
                    {'id': r[0], 'name': r[1], 'price': r[2], 'category': r[3]}
                    for r in cur.fetchall()
                ]
        except Exception as e:
            return HttpResponse(f"<pre>SQL error: {e}</pre>", status=500)
    else:
        results = []
    return render(request, 'shop/products.html', {'results': results, 'query': q, 'mode': 'VULNERABLE'})

# ---------- SAFE SEARCH (for comparison / teaching) ----------
def fixed_search(request):
    q = request.GET.get('q', '')
    # SAFE: parameterized query — input can never change query structure
    sql = "SELECT id, name, price, category FROM shop_product WHERE name LIKE %s OR description LIKE %s"
    with connection.cursor() as cur:
        cur.execute(sql, [f'%{q}%', f'%{q}%'])
        results = [{'id': r[0], 'name': r[1], 'price': r[2], 'category': r[3]} for r in cur.fetchall()]
    return render(request, 'shop/fixed_search.html', {'results': results, 'query': q, 'mode': 'SAFE'})

# ---------- VULNERABLE PRODUCT DETAIL (numeric injection) ----------
def product_detail(request, product_id):
    # VULN: f-string of a URL parameter (attacker controls /product/<id>/)
    sql = f"SELECT id, name, description, price, category FROM shop_product WHERE id = {product_id}"
    try:
        with connection.cursor() as cur:
            cur.execute(sql)
            row = cur.fetchone()
    except Exception as e:
        return HttpResponse(f"<pre>SQL error: {e}</pre>", status=500)
    if not row:
        return HttpResponse('Not found', status=404)
    product = {'id': row[0], 'name': row[1], 'description': row[2],
               'price': row[3], 'category': row[4]}
    comments = Comment.objects.filter(product_id=row[0]).order_by('-created_at')
    return render(request, 'shop/product_detail.html', {'p': product, 'comments': comments})

# ---------- VULNERABLE PROFILE (UNION-based demo target) ----------
@login_required
def profile(request):
    uid = request.GET.get('id', request.user.id)
    # VULN: attacker-controlled 'id' GET parameter
    sql = f"SELECT id, username, first_name, email FROM auth_user WHERE id = {uid}"
    try:
        with connection.cursor() as cur:
            cur.execute(sql)
            row = cur.fetchone()
    except Exception as e:
        return HttpResponse(f"<pre>SQL error: {e}</pre>", status=500)
    if not row:
        return HttpResponse('No such user', status=404)
    return render(request, 'shop/profile.html',
                  {'username': row[1], 'full_name': row[2], 'email': row[3], 'via': 'profile'})