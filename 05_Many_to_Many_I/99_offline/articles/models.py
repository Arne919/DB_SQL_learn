# articles/models.py
from django.db import models
from django.conf import settings

class Article(models.Model):
    # user에 대한 Model 명은
        # 1. 다른 앱에 있음
        # 2. User는 조금 복잡한 관계임..
    # settings 에 적어둔 AUTH_USER_MODEL을 쓰기로했다.
    # 1:N의 관계는 내가 참조하고 있는 대상이 삭제됐을때,
    # 나 (N의 입장인 모델)을 어떻게 처리할지도 같이 적어줘야함
    # ForeignKey를 정의하는 N의 입장에만 필드를 추가하는 이유는?
        # 1의 입장에서는 N이 없을 수도 있다. : 애초에 관계가  0 <= N <= K
        # 그래서, user 필드를 정의해둔 Article 입장에서는
        # python에서 Article 클래스의 instance를 생성했을때,
        # 자기네 변수명에 user가 있으니까, aritcle_instance.user 라고
        # 직접적으로 호출해서 사용할 수 있다. 아주 편하다.
    user = models.ForeignKey(
        # 참조 대상 모델에게 알아서 역참조_매니저를 붙여준다.
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # user = models.ManyToManyField(settings.AUTH_USER_MODEL,)
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 컬럼명 : 이 변수에 저장되는 값이 어떤 값인지를 나타내야햄
    # 지금 만들려는 기능 : 좋아요를 누른 유저 목록을 나타냄.
    # MTMF -> M:N 관계라고 했으니... 당연히 상대방 Model이 누군지 적어줘야한다.
    # 이제 Article은 자기와 (좋아요를 위한) 관계 맺고 있는 User 정보를
    # like_users를 통해서 쉽게 조회 할 수 있게 되었다.
        # 근데, 여전히 User는??? User class에 아무것도 정의가 안되어 있으니
        # 여기서도 1:N의 규칙에 맞춰서 모델명_set으로 접근할수 있게 매니저를 달아준다. 
    # 만약, 상대방이든, 나든, 역참조매니저 명이 중복되는 경우가 발생하면
    # 기능적으로 불가능해지므로, 이런한 상황에 대해서만 특별히, 
    # 역참조 매니저명을 별도로 지정해줘야 한다.
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        # 변수명은 항상 기능에 충실하게 이름을 지어준다.
        related_name='like_articles'
    )

'''
    근데 문제는 1:N만 가지고는 우리 세상에 있는 각종 관계를 모두 표현할수 없더라.
    환자 : 의사 관계를 봤더니,
    환자 1은 의사 1, 2, 3 모두에게 진찰을 받을 수 있었고,
    의사 1은 환자 1, 2, 3 모두를 진찰 할 수 있더라.
    -> 환자와 의사관의 관계가 1:N이 아니라 M:N 형태가 되어야 하더라.

    -> 어라? 그럼 그냥 
    환자랑 의사가 1:N의 관계이면서
    의사랑 환자가 1:N의 관계가 되도록 하면 되지 않을까?
    -> M:N이다.

    -> 대신에... 이렇게 마구잡이로 1:N의 관계를 데이터베이스 설정할때 만들면
    1. 컬럼이 너무 복잡해 진다.
    2. 의사랑 환자가 1:N의 관계를 맺는 경우가 하나가 아니라 여러개가 될 경우,
       헷갈리는 경우도 너무 많이 나온다.
    3. 그래서, 의사(1):환자(N) 과 환자(1):의사(N)은 사실.. 서로 다른 관계가 아니라
       결국 `진료` 라는 하나의 관계인데... 컬럼은 2개가 만들어진다.
        - 관리가 어려워진다.
    
    - 그래서 해결방법은 
    그 위에서 말한 환자와 의사의 서로에 대한 1:N관계를 그냥 다른테이블에 박아버리자.
'''

# class Reservation(models.Model):
#     doctor = models.ForeignKey()
#     patiend = models.ForeignKey()

# 원래 게시글:작성자의 M:N 관계 (좋아요 기능을 위한) 을 만든다면
# 이렇게 모델을 만들어야 한다.
# 문제? 아쉬운점? 
    # - 1의 입장이 될, Article과 User가 정작 자기랑 관계 맺고 있는
    # 상대방 User와 Article을 찾기가 번거롭다...
    # 그래서 django는 MTMF라는걸 제공해 준다.
# class ArticleLikeUsers(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)


'''
    그럼 중개모델은 어떨때 써야 하느냐?
    M:N 관계를 형성 할때, 추가적인 필드가 필요할때...
    -> 서로가 서로 관계를 맺고 있는 상태를 만들때, 
        관계가 T/F냐 말고도 다른 정보도 저장해야 할때

    환자:의사
    환자1이 의사1에게 진료를 받는데, `몇시에` 받느냐. 등
    -> `몇 시`정보를 저장할 수 있는 공간도 만들어 줘야함
        -> MTMF로 만들어진 테이블은 그런건 저장못함.
        -> MTMF로 만들어진 테이블은 오로지 서로의 id만 저장하도록 만들어줌.
        -> 그게 가장 기본적인 모양이기 떄문에.
'''