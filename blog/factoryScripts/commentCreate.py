from blog.factory import BlogCommentFactory


comments = []
for _ in range(90):
    BlogCommentFactory.create()
        
