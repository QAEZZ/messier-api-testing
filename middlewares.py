import aiohttp_jinja2
import jinja2 # I think I imported too much lmao
from aiohttp_jinja2 import *
from aiohttp import web


async def handle_404(request):
    return aiohttp_jinja2.render_template('./static/html/errors/404.html', request, {})


async def handle_500(request):
    return aiohttp_jinja2.render_template('./static/html/errors/500.html', request, {})


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):

        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await override(request)

            return response

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise

    return error_middleware


def setup_middlewares(app):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('.'))
    app.router.add_static('/static', "static")

    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)