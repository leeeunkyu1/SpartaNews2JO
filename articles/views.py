from django.shortcuts import render

# Create your views here.
class CommentsView(APIView):
    # 댓글조회 나중에 article 조회로 옮길 것
    def get(self,request, article_pk):
        pass
    # 댓글 작성
    def post(self, request, article_pk):
        pass
    # 댓글 수정
    def put(self, request, article_pk):
        pass
    # 댓글 삭제
    def delete(self, request, article_pk):
        pass