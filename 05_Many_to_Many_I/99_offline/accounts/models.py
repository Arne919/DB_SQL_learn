from django.db import models
from django.contrib.auth.models import AbstractUser


# User는 Article과 1:N의 형태다.
# 근데, User는 Article이 없을 수도 있다.
# 그리고, 그 1:N 관계는 Article class에 만들어 뒀다.
# 그럼, 만약, User 1번이 작성한 게시글 목록을 보려고 한다면?
# 지금 정의해둔 class 상태로는 접근 할 수 있는 방법이 없다.
    # 그래서, django가 이런 1의 입장에서도, 쉽게 N들을 불러올 수 있도록
    # manager를 만들어 준다.
# Model.Manager.QuerySet API() -> ORM이라고 불렀었다.
    # Manager -> objects 하나 뿐이었는데...
# Model.referencesmodel_set.QuerySet API
    # 이런식으로, 나를 참조하고있는 모델명_set 형식의 매니저도 붙여준다.
    # User.article_set.all() -> 나를 참조하고있는 모든 게시글 정보 조회
class User(AbstractUser):
    pass
