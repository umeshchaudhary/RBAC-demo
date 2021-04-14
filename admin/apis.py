from fastapi import APIRouter

router = APIRouter(
  prefix='/',
  tags=['admin'],
)


@router.post('/signin')
def sign_in(user):
    pass
