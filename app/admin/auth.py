from app.users.dependencies import get_cur_user
from sqladmin.authentication import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.users.auth import check_user, create_acces_token
from typing import Optional


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request, user_data=None) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await check_user(input_email=email, input_pass=password)
        if user:
            acces_token = create_acces_token({"sub": str(user.id)})
            request.session.update({"token": acces_token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse] :
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        user = await get_cur_user(token)

        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)



authentication_backend = AdminAuth(secret_key="...")
