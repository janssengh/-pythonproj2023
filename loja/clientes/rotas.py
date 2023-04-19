import secrets

from flask import render_template, redirect, url_for, flash, request, session, make_response
from loja import app, db, bcrypt
from .forms import CadastroClienteForm, ClienteLoginForm
from .model import Client, ClientOrder

from flask_login import login_required, current_user, login_user, logout_user
import pdfkit
import stripe


publishable_key = 'pk_test_51MuGtwGhyM6JqwPtVWXLJqVrAcyJfZXHUHMBX46BU895l6ypXlJ0aKk8LDuPw3TzYIYmO6901OPQc2XDcIhiYcbq00VbWXO4tP'
stripe.api_key = 'sk_test_51MuGtwGhyM6JqwPtVePPrdpZ2TJqDwI17sJ98o4sVtKDErlHnd0lNUksbd2HMdvMmMmu68cj5xOZt3eewYPrcDHS008a0778UW'

@app.route('/pagamento', methods=['POST'])
@login_required
def pagamento():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')



    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Loja_Flask',
        amount=amount,
        currency='brl',
    )
    print(f'invoice: {invoice}')
    client_order = ClientOrder.query.filter_by(client_id=current_user.id, invoice=invoice).order_by(
        ClientOrder.id.desc()).first()
    print(f'status: {ClientOrder.status}')
    client_order.status = 'Pago'
    db.session.commit()
    return redirect(url_for('obrigado'))


@app.route('/obrigado')
def obrigado():
    return render_template('cliente/obrigado.html')

@app.route('/cliente/cadastrar', methods=['GET','POST'])
def cadastrar_clientes():
    form = CadastroClienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Client(name=form.name.data, username=form.username.data, email=form.email.data,
                              password=hash_password, country=form.country.data, contact=form.contact.data,
                              city=form.city.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(cadastrar)
        flash(f'{form.name.data} Obrigado por cadastrar!', 'success')
        db.session.commit()
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/cliente.html', form=form)

@app.route('/cliente/login', methods=['GET','POST'])
def clienteLogin():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        user = Client.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Voce está logado!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'Senha/E-mail incorretos ou não cadastrados!', 'danger')
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/login.html', form=form)

@app.route('/cliente/logout')
def cliente_logout():
    logout_user()
    return redirect(url_for('home'))


def atualizarlojaCarro():
    for _key, produto in session['LojainCarrinho'].items():
        session.modified = True
        del produto['image']
        del produto['colors']

    return atualizarlojaCarro


@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated:
        client_id = current_user.id
        invoice = secrets.token_hex(5)
        atualizarlojaCarro()

        try:
            p_order = ClientOrder(invoice=invoice, client_id=client_id, order=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash(f'Seu pedido foi adicionado com sucesso !', 'success')
            return redirect(url_for('pedidos', invoice=invoice))
        except Exception as e:
            print(e)
            flash(f'Não foi possível processar o seu pedido !', 'danger')
            return redirect(url_for('getCart'))

@app.route('/pedidos/<invoice>')
@login_required
def pedidos(invoice):
    if current_user.is_authenticated:
        gTotal = 0
        subTotal = 0
        client_id = current_user.id
        cliente = Client.query.filter_by(id=client_id).first()
        pedidos = ClientOrder.query.filter_by(client_id=client_id, invoice=invoice).order_by(ClientOrder.id.desc()).first()
        for key, produto in pedidos.order.items():
            desconto = (produto['discount']/100) * float(produto['price'])
            subTotal += float(produto['price']) * int(produto['quantity'])
            subTotal -= desconto
            imposto = ("%.2f" % (0.6 * float(subTotal)))
            gTotal = float("%.2f" % (1.06 * subTotal))
    else:
        return redirect(url_for('ClienteLogin'))
    return render_template('cliente/pedido.html', notafiscal=invoice, imposto=imposto, subTotal=subTotal,
                           gTotal=gTotal, cliente=cliente, pedidos=pedidos)

@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        gTotal = 0
        subTotal = 0
        client_id = current_user.id
        if request.method == "POST":

            cliente = Client.query.filter_by(id=client_id).first()
            pedidos = ClientOrder.query.filter_by(client_id=client_id, invoice=invoice).order_by(
                ClientOrder.id.desc()).first()
            # .pedido se refere ao campo no model class ClientePedido
            for key, produto in pedidos.order.items():
                desconto = (produto['discount'] / 100) * float(produto['price'])
                subTotal += float(produto['price']) * int(produto['quantity'])
                subTotal -= desconto
                imposto = ("%.2f" % (0.6 * float(subTotal)))
                gTotal = float("%.2f" % (1.06 * subTotal))


            rendered = render_template('cliente/pdf.html', notafiscal=invoice, imposto=imposto,
                                       subTotal=subTotal, gTotal=gTotal, cliente=cliente, pedidos=pedidos)


            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            # gerar pdf
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'attached;filename='+ invoice+'. pdf'
            return response
    return redirect(url_for('pedidos'))




