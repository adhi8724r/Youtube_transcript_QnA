from pydantic import BaseModel, computed_field

class YoutubeURL(BaseModel):
    youtube_url: str

    @computed_field
    @property
    def id(self) -> str:
        id = self.youtube_url.split('v=')[1].split('&')[0]
        return id
