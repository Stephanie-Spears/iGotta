from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_babel import _, get_locale
from flask_googlemaps import Map
from flask_login import current_user, login_required
from langdetect import detect

from iGottaPackage import db, images
from iGottaPackage.main import bp
from iGottaPackage.main.forms import EditProfileForm, PostForm, SearchForm, BathroomForm
from iGottaPackage.models import User, Post, Bathroom
from iGottaPackage.translate import translate


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_on = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = detect(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now up!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'), posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'], request.form['source_language'], request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts, next_url=next_url, prev_url=prev_url)


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash(_('Post not found.'))
        return redirect(url_for('main.index'))
    if post.author.id != current_user.id:
        flash(_('You cannot delete this post.'))
        return redirect(url_for('main.index'))
    db.session.delete(post)
    db.session.commit()
    flash(_('Your post has been deleted.'))
    return redirect(url_for('main.index'))


@bp.route('/add_bathroom/', methods=['GET', 'POST'])
@login_required
def add_bathroom():
    form = BathroomForm()
    if form.validate_on_submit():
        filename = images.save(request.files['bathroom_image'])
        url = images.url(filename)
        new_bathroom = Bathroom(form.bathroom_name.data, form.bathroom_about.data, form.bathroom_address.data, filename, url)
        db.session.add(new_bathroom)
        db.session.commit()
        flash(_('The bathroom: {} is now up!').format(new_bathroom.bathroom_name))
        return redirect(url_for('main.bathroom', bathroom_name=new_bathroom.bathroom_name))
    return render_template('add_bathroom.html', form=form)


@bp.route('/bathroom/<bathroom_name>')
@login_required
def bathroom(bathroom_name):
    new_bathroom = Bathroom.query.filter_by(bathroom_name=bathroom_name).first_or_404()
    return render_template('bathroom.html', bathroom=new_bathroom)
    # page = request.args.get('page', 1, type=int)
    # bathroom_posts = bathroom.bathroom_posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('main.bathroom', bathroom_name=bathroom.bathroom_name, page=bathroom_posts.next_num) \
    #     if bathroom_posts.has_next else None
    # prev_url = url_for('main.bathroom', bathroom_name=bathroom.bathroom_name, page=bathroom_posts.prev_num) \
    #     if bathroom_posts.has_prev else None
    # return render_template('bathroom.html', bathroom=bathroom, bathroom_posts=bathroom_posts.items, next_url=next_url, prev_url=prev_url)


# todo: reinstigate popup html
# @bp.route('/bathroom/<bathroom_name>/popup')
# @login_required
# def bathroom_popup(bathroom_name):
#     bathroom = Bathroom.query.filter_by(bathroom_name=bathroom_name).first_or_404()
#     return render_template('bathroom_popup.html', bathroom=bathroom)


@bp.route('/maps')
@login_required
def maps():
    # todo: remove hardcoded bathrooms
    bathroommap = Map(
        identifier="bathroommap",
        style="height:100%;width:100%;margin:0;padding:0;",
        lat=45.519322,
        lng=-122.623073,
        markers=[
            {
                'icon': 'static/img/toilet-icon.png',
                'lat': 45.520705,
                'lng': -122.677570,
                'infobox': "<h1>Pu-Pu-Punk</h1><br><b>So punk. The most hardcore toilet in Portland. A literal shithole.</b>"
            },
            {
                'icon': 'static/img/toilet-icon.png',
                'lat': 45.511835,
                'lng': -122.623733,
                'infobox': "<h1>Taco Toots-day</h1><br><b>Located right inside Portland's spiciest Burrito spot, Anillo de Fuego!</b>"
            }
        ]
    )
    return render_template('maps.html', bathroommap=bathroommap)
    # todo: remove below if flask ext is adequate
    # gmaps = googlemaps.Client(key=current_app.config['GOOGLEMAPS_KEY'])
    # geolocate_results = gmaps.geolocate(consider_ip=True)
    # geocode_result = gmaps.geocode('2755 SE 32nd, Portland, OR')
    # reverse_geocode_result = gmaps.reverse_geocode((45.507889, -122.613662))
    # now = datetime.now()
    # # directions_result = gmaps.directions(geocode_result, reverse_geocode_result, mode="transit", departure_time=now)
    # return render_template('maps.html')