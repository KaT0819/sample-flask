# sample-flask


https://github.com/jimdevops19/FlaskSeries.git

## Install
```
pip install flask

flask --version
```

## run
```
flask run
```


## setting

mac
```
set FLASK_APP=market.py

# debug mode
set FLASK_DEBUG=1

```

windows powershell
```
$ENV:FLASK_APP='market.py'

# debug mode
$ENV:FLASK_DEBUG='1'
```

## DB
```
python 

from market.models import db

db.drop_all()
db.create_all()

from market.models import Item, User

u1 = User(username='user1', password='123456', email='user1@user.com')
db.session.add(u1)
db.session.commit()

u2 = User(username='user2', password='123456', email='user2@user.com')
db.session.add(u2)
db.session.commit()

User.query.all()


i1 = Item(name= '電話', barcode= '893212299897', price= 50000, description='description1')
db.session.add(i1)
db.session.commit()

i2 = Item(name= 'ラップトップ', barcode= '123456789012', price= 90000, description='description2')
db.session.add(i2)
db.session.commit()

i3 = Item(name= 'キーボード', barcode= '987654321012', price= 1500, description='description3')
db.session.add(i3)
db.session.commit()


Item.query.all()

item1 = Item.query.filter_by(name='電話').first()
item1.owner = User.query.filter_by(username='user1').first().id
db.session.add(item1)
db.session.commit()
```
