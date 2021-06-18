from flask import render_template, request, redirect, url_for
from modules.dao import SearchDao
from main import app
from modules.config import db

search_dao = SearchDao(db)

@app.route('/')
def index():
    return render_template('lista.html', titulo='Pesquisa SGI - Usuário')


@app.route('/indexSearch', methods=['POST', ])
def indexSearch():
    search = request.form['search'].upper()
    searchRadio = request.form['searchRadio'].upper()

    if search is None or search == '':
        return redirect(url_for('index'))
    elif searchRadio == 'USUARIO':
        lista = search_dao.listarSearch(search)
        return render_template('lista.html', titulo='Pesquisa SGI - Usuário', cadastros=lista)
    else:
        lista = search_dao.listarSearchResp(search)
        return render_template('lista.html', titulo='Pesquisa SGI - Usuário', cadastros=lista)


@app.route('/objt')
def objt():
    return render_template('listaObjetos.html', titulo='Pesquisa SGI - Objeto')

@app.route('/indexSearchObj', methods=['POST', ])
def indexSearchObj():
    search = request.form['search'].upper()
    searchRadio = request.form['searchRadio'].upper()

    if search is None or search == '':
        return redirect(url_for('objt'))
    elif searchRadio == 'OBJETO':
        lista = search_dao.listarSearchObj(search)
        return render_template('listaObjetos.html', titulo='Pesquisa SGI - Objeto', cadastros=lista)
    else:
        lista = search_dao.listarSearchRespObj(search)
        return render_template('listaObjetos.html', titulo='Pesquisa SGI - Objeto', cadastros=lista)