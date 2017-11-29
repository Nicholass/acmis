from cms.models import Category

Category.objects.create(name='Drawing', route='drawing').save()
Category.objects.create(name='Map', route='map').save()
Category.objects.create(name='News', route='news').save()
Category.objects.create(name='Photo', route='photo').save()
Category.objects.create(name='Prose', route='prose').save()
Category.objects.create(name='Report', route='report').save()

categories = Category.objects.all()

for category in categories:
  category.publish()

print('categories created succefull')