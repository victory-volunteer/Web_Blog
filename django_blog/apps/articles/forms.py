from django import forms


class CommentForm(forms.Form):
    # 提交评论
    pass
    email01 = forms.EmailField(required=True, error_messages={'required': u'邮箱格式不正确'})
    username01 = forms.CharField(
        required=True, min_length=3, max_length=5,
        error_messages={
            "required": "用户名不能为空",
            "min_length": "用户名不能小于3位",
            "max_length": "不能超过5位", }
    )

