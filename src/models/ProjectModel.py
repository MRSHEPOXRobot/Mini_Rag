from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):

        # حوّل الـ project من Pydantic Model إلى Dictionary،
        # استخدم أسماء الـ aliases لو موجودة، واستبعد الـ fields اللي المستخدم ماحددهاش
        # وبعد كده خزّن الـ Dictionary كـ Document جديد في MongoDB، واستقبل نتيجة عملية الإدخال في result.
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        # by_alias=True هات الإسم المستعار , exclude_unset=True خد القيم الأفتراضية
        project._id = result.inserted_id

        return project

    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one({
            "project_id": project_id
        })
        #find_one return dictionary.

        if record is None:
            # create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project

        return Project(**record) #هيتحول من dict ل Project

    async def get_all_projects(self, page: int = 1, page_size: int = 10): #Default Values.

        # count total number of documents
        total_documents = await self.collection.count_documents({})

        # calculate total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip( (page - 1) * page_size ).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document) #هيتحول من dict ل Project
            )

        return projects, total_pages
