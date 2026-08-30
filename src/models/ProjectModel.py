from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    # عملنا فانكشن بتعرف ال object وبتنادي فيه على ال init_connection إلي من نوع async
    # علشان أنا مكنتش هعرف أنادي على ال async init_connection داخل ال __init__ لإنها من نوع async
    @classmethod #define static method
    async def create_instance(cls, db_client: object):#class method
        instance = cls(db_client) # كده أنا بقوله يا كلاس خد ال db_client وهو كده نادى على ال init()
        await instance.init_collection()
        return instance


    async def init_collection(self):#async function لإن احنا بنتعامل مع ال Mongodb
        #إلي بنستخدم فيها ال Motors إلي معتمد على ال AsyncIOMotorClient ف كل عملياته async ف لازم الفانكشنز كمان تبقى async
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_project(self, project: Project):

        # حوّل الـ project من Pydantic Model إلى Dictionary،
        # استخدم أسماء الـ aliases لو موجودة، واستبعد الـ fields اللي المستخدم ماحددهاش
        # وبعد كده خزّن الـ Dictionary كـ Document جديد في MongoDB، واستقبل نتيجة عملية الإدخال في result.
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        # الفانكشن insert_one بتاخد dictionary
        # by_alias=True هات الإسم المستعار , exclude_unset=True خد القيم الأفتراضية
        project.id = result.inserted_id

        return project

    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one({
            "project_id": project_id
        })
        #find_one return dictionary.
        # الـ project_id
        # ده Application-level ID أنت اللي معرفه:
        # "project_id": "2"
        # وده ممكن يكون String عادي.

        if record is None:
            # create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project

        return Project(**record) #هيتحول من dict ل Project Model

    async def get_all_projects(self, page: int = 1, page_size: int = 10): #Default Values.

        # count total number of documents
        total_documents = await self.collection.count_documents({})

        # calculate total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip( (page - 1) * page_size ).limit(page_size)
        # "جهّزلي Cursor أقدر ألف بيه على الـ documents" وليس: "هاتلي الـ documents دلوقتي لذلك مفيش await هنا.
        projects = []
        async for document in cursor: # async
            #لإن cursor جاي من motor و motor ده async
            projects.append(
                Project(**document) #هيتحول من dict ل Project
            )

        return projects, total_pages
