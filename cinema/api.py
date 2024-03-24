from ninja import Router, UploadedFile, File, Form
from ninja.pagination import paginate, PageNumberPagination
from typing import List, Optional

from .models import Movie
from .schemas import ExtraMessage, MovieIn, MovieOut


router = Router()


@router.post("/", response={201: MovieOut})
def create_movie(
    request,
    payload: Form[MovieIn],
    poster_file: Optional[UploadedFile] = File(None),
    trailer_file: Optional[UploadedFile] = File(None),
):
    payload_dict = payload.dict(exclude_unset=True)
    movie = Movie(**payload_dict)
    if not poster_file or trailer_file:
        movie.save()
    if poster_file:
        movie.poster.save(movie.name, poster_file)  # will save model instance as well
    if trailer_file:
        movie.trailer.save(movie.name, trailer_file)  # will save model instance as well
    return movie


@router.get("/{movie_id}", response={200: MovieOut, 404: ExtraMessage})
def get_movie(request, movie_id: int):
    try:
        movie = Movie.objects.get(id=movie_id)
    except:
        return 404, {"message": "Movie with id not found"}
    return movie


@router.get("/", response=List[MovieOut])
@paginate(PageNumberPagination, page_size=50)
def list_movies(request):
    qs = Movie.objects.order_by("-ranking")
    return qs


@router.put("/{movie_id}", response={200: MovieOut, 404: ExtraMessage})
def update_movie(
    request,
    movie_id: int,
    payload: Form[MovieIn],
    poster_file: Optional[UploadedFile] = File(None),
    trailer_file: Optional[UploadedFile] = File(None),
):
    try:
        movie = Movie.objects.get(id=movie_id)
    except:
        return 404, {"message": "Movie with id not found"}

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(movie, attr, value)

    if not poster_file or trailer_file:
        movie.save()
    if poster_file:
        movie.poster.save(movie.name, poster_file)  # will save model instance as well
    if trailer_file:
        movie.trailer.save(movie.name, trailer_file)  # will save model instance as well
    return movie


@router.delete("/{movie_id}", response={204: ExtraMessage, 404: ExtraMessage})
def delete_movie(request, movie_id: int):
    try:
        movie = Movie.objects.get(id=movie_id)
    except:
        return 404, {"message": "Movie with id not found"}

    movie.delete()
    return 204, {"message": "Success"}
