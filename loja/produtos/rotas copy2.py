import secrets, os

from flask import render_template, request, redirect, url_for, flash, session,current_app

from loja import app, db, photos
from loja.produtos.forms import Addprodutos
from loja.produtos.models import Brand, Category, Product

def marcas():
    marcas = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return marcas

def categorias():
    categorias = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return categorias

@app.route('/')
def home():
    pagina = request.args.get('pagina', 1, type=int)
    produtos = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=pagina, per_page=4)
    return render_template('produtos/index.html', produtos=produtos, marcas=marcas(), categorias=categorias())

@app.route('/search', methods=['GET','POST'])
def search():

    if request.method == 'POST':
        form = request.form
        search_value = form['search-string']
        search = "%{0}%".format(search_value)
        produtos = Product.query.filter(Product.name.like(search)).all()
        return render_template('pesquisar.html', produtos=produtos, marcas=marcas(), categorias=categorias())
    else:
        return redirect('/')

@app.route('/marca/<int:id>')
def get_marca(id):
    get_m = Brand.query.filter_by(id=id).first_or_404()
    pagina = request.args.get('pagina', 1, type=int)

    marca = Product.query.filter_by(marca=get_m).paginate(page=pagina, per_page=4)
    marcas = Brand.query.join(Product, (Brand.id == Product.marca_id)).all()
    categorias = Category.query.join(Product, (Category.id == Product.categoria_id)).all()
    return render_template('produtos/index.html', marca=marca, marcas=marcas, categorias=categorias,
                           get_m=get_m)

@app.route('/produto/<int:id>')
def pagina_unica(id):
    produto = Product.query.get_or_404(id)

    marcas = Brand.query.join(Product, (Brand.id == Product.marca_id)).all()
    categorias = Category.query.join(Product, (Category.id == Product.categoria_id)).all()

    return render_template('produtos/pagina_unica.html', produto=produto, marcas=marcas, categorias=categorias)

@app.route('/categorias/<int:id>')
def get_categoria(id):
    pagina = request.args.get('pagina', 1, type=int)

    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Product.query.filter_by(categoria=get_cat).paginate(page=pagina, per_page=4)
    marcas = Brand.query.join(Product, (Brand.id == Product.marca_id)).all()
    categorias = Category.query.join(Product,(Category.id == Product.categoria_id)).all()
    return render_template('produtos/index.html', get_cat_prod=get_cat_prod, categorias=categorias, marcas=marcas,
                           get_cat=get_cat)

@app.route('/addmarca', methods=['GET','POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('marca')
        brand = Brand(name=getmarca)
        db.session.add(brand)
        flash(f'A marca {getmarca} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('produtos/addmarca.html', brand='brand')

@app.route('/updatemarca/<int:id>' , methods=['GET','POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatemarca = Brand.query.get_or_404(id)
    marcas = request.form.get('marca')
    if request.method == 'POST':
        updatemarca.name = marcas
        flash(f'Seu Fabricante foi Atualizado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))
    return render_template('produtos/updatemarca.html', titulo='Atualizar Fabricantes', updatemarca=updatemarca)

@app.route('/deletemarca/<int:id>' , methods=['POST'])
def deletemarca(id):

    marcas = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(marcas)
        db.session.commit()
        flash(f'A Marca {marcas.name} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Marca {marcas.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))

@app.route('/updatecat/<int:id>' , methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    updatecat = Category.query.get_or_404(id)
    categorias = request.form.get('categoria')
    if request.method == 'POST':
        updatecat.name = categorias
        flash(f'Sua Categoria foi Atualizada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('produtos/updatemarca.html', titulo='Atualizar Categoria', updatecat=updatecat)

@app.route('/deletecategoria/<int:id>' , methods=['POST'])
def deletecategoria(id):

    categorias = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(categorias)
        db.session.commit()
        flash(f'A Categoria {categorias.name} foi excluída com sucesso!', 'success')
        return redirect(url_for('admin'))
    flash(f'A Categoria {categorias.name} não foi excluída!', 'warning')
    return redirect(url_for('admin'))

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('categoria')
        category = Category(name=getmarca)
        db.session.add(category)
        flash(f'A categoria {getmarca} foi cadastrada com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('produtos/addmarca.html')

@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))

    marcas = Brand.query.all()
    categorias = Category.query.all()
    form = Addprodutos(request.form)
    if request.method == "POST":

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        discription = form.discription.data

        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        print(image_1)

        addpro = Product(name=name, price=price, discount=discount, stock=stock, colors=colors, discription=discription,
                         brand_id=marca, category_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3)

        db.session.add(addpro)
        flash(f'Produto {name} foi cadastrado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('admin'))


    return render_template('produtos/addproduto.html', form=form, titulo='Cadastro de Produto', marcas=marcas, categorias=categorias)

@app.route('/updateproduto/<int:id>' , methods=['GET','POST'])
def updateproduto(id):
    marcas = Brand.query.all()
    categorias = Category.query.all()
    produto = Product.query.get_or_404(id)

    marca = request.form.get('marca')
    categoria = request.form.get('categoria')

    form = Addprodutos(request.form)

    if request.method == "POST":
        produto.name = form.name.data
        produto.price = form.price.data
        produto.discount = form.discount.data

        produto.brand_id = marca
        produto.category_id = categoria

        produto.stock = form.stock.data
        produto.colors = form.colors.data
        produto.discription = form.discription.data

        if request.files.get('image_1'):
            try:
                # remove a imagem do diretório
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                # remove a imagem do diretório
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                # remove a imagem do diretório
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'Produto foi atualizado com sucesso!', 'success')
        return redirect(url_for('admin'))

    form.name.data = produto.name
    form.price.data = produto.price
    form.discount.data = produto.discount
    form.stock.data = produto.stock
    form.colors.data = produto.colors
    form.discription.data = produto.discription

    return render_template('produtos/updateproduto.html', titulo='Atualizar Produtos', form=form, marcas=marcas,
                           categorias=categorias, produto=produto)

@app.route('/deleteproduto/<int:id>' , methods=['POST'])
def deleteproduto(id):

    produto = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            if request.files.get('image_1'):
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produto.image_3))
        except Exception as e:
            print('Erro ')


        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('admin'))

    flash(f'Produto {produto.name} foi excluído com sucesso!', 'success')

    return redirect(url_for('admin'))