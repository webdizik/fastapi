import requests


response = requests.post(
    "http://127.0.0.1:8000/api/v1/posts",
    json={
        "title": "Куплю что-нибудь",
        "description": "Недорогое.",
        "ad_author": "Петя",
        },
    )

print(response.status_code)
print(response.json())

response = requests.get("http://127.0.0.1:8080/posts/1")
print(response.status_code)
print(response.json())

# response = await session.patch(
#     "http://127.0.0.1:8080/posts/1",
#     json={"title": "new_post_1"},
# )
# print(response.status)
# print(await response.json())

# response = await session.delete(
#     "http://127.0.0.1:8080/posts/1",
# )
# print(response.status)
# print(await response.json())
