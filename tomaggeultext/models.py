from django.db import models
from django.utils import timezone

from genre.models import Genre

from user.models import TMAuthor, TMUser

class TMSeries(models.Model):
    series_id = models.AutoField(primary_key=True)
    series_title = models.CharField(max_length=30)
    introduce = models.CharField(max_length=1000, null=True, blank=True)
    is_paid_subs = models.BooleanField(default=False)
    series_genre = models.ManyToManyField(Genre, related_name='series_genre')
    last_uploaded_date = models.DateTimeField(default = timezone.now)
    tomag_num_total = models.PositiveIntegerField(default=0)     #토막글 수 종합
    heart_num_total = models.PositiveIntegerField(default=0)     #공감 수
    comment_num_total = models.PositiveIntegerField(default=0)   #댓글 수 종합
    views_num_total = models.PositiveIntegerField(default=0)     #조회 수 종합
    writer = models.ForeignKey(TMAuthor, on_delete=models.CASCADE, related_name='series')

    def __str__(self):
        return self.series_title

class TMText(models.Model):
    text_id = models.AutoField(primary_key=True)
    text_title = models.CharField(max_length=30)
    main_sentence = models.CharField(max_length=200, null=True, blank=True, default="Main sentence")
    text_content = models.CharField(max_length=5000)
    text_genre =  models.ManyToManyField(Genre, related_name='text_genre')
    heart_num = models.PositiveIntegerField(default=0)     #공감 수
    comment_num = models.PositiveIntegerField(default=0)   #댓글 수
    views_num = models.PositiveIntegerField(default=0)     #조회 수
    date_of_write = models.DateField(default = timezone.now)
    writer = models.ForeignKey(TMAuthor, on_delete=models.CASCADE, related_name='text')
    series = models.ForeignKey(TMSeries, on_delete=models.CASCADE, null=True, blank=True, related_name='text')
    text_cover = models.ImageField(upload_to='covers',default='../static/img/no-image.png')
    def __str__(self):
        return self.text_title

class Comment(models.Model):
    date_of_comment = models.DateField(default = timezone.now)
    comment_content = models.CharField(max_length=100)
    is_report = models.BooleanField(default=False)
    tmtext = models.ForeignKey(TMText, on_delete=models.CASCADE, related_name='comment')
    tmuser = models.ForeignKey(TMUser, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return self.tmuser.nickname + ':' + self.comment_content

class Paid_subscription(models.Model):
    tmuser = models.ForeignKey(TMUser, on_delete=models.CASCADE)
    tmseries = models.ForeignKey(TMSeries, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    use_points = models.PositiveIntegerField(default=0)
    remaining_points = models.PositiveIntegerField(default=0)
    payment = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.tmuser.nickname + " paid subs " + self.tmseries.writer.author_name+ '\'s ' + self.tmseries.series_title

class Subscription(models.Model):
    tmuser = models.ForeignKey(TMUser, on_delete=models.CASCADE)
    tmseries = models.ForeignKey(TMSeries, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.tmuser.nickname + " subs " + self.tmseries.writer.author_name+ '\'s ' + self.tmseries.series_title

class Delivery(models.Model):
    tmuser = models.ForeignKey(TMUser, on_delete=models.CASCADE)
    paid_subs = models.ForeignKey(Paid_subscription, on_delete=models.CASCADE)
    adress = models.CharField(max_length=200)
    delivery_time = models.DateTimeField(default=timezone.now)
    delivery_status = models.BooleanField(default=False)
    delivery_copletion = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.tmuser.nickname + str(self.delivery_time)