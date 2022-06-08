from fastapi import  APIRouter, Depends, Path, status, Body, File, UploadFile
from accounts.utils import get_current_user_admin, get_current_user
from .models import CategoryModel, ProductsModel, CommentsModel
from fastapi.responses import JSONResponse
from config.settings import BASE_DIR
from datetime import datetime
from accounts.schema import UserSchema
import os
from .schema import ProductSchema


router = APIRouter(prefix='/product', tags=['produucts'])


@router.get('/all/ctegories/', response_model=list[CategoryModel], response_model_include=['name',])
async def all_category():
    categories = await CategoryModel.objects.all()
    return categories


categoryResponse = CategoryModel.get_pydantic(include={"name":..., "all_product": {"id", "name"}})
@router.get('/get/category/{name:str}/', response_model=categoryResponse)
async def get_category(name:str=Path(...)):
    category = await  CategoryModel.objects.prefetch_related('all_product').get_or_none(name=name, all_product__publish=True)

    if category is None:
        return JSONResponse(status_code = 404, content='nothing found anything')

    return category


productResponse = ProductsModel.get_pydantic(exclude={'id':...,'publish':..., 'created':..., 
                'category':{'id'}, 'all_image':{'id'}, 'all_comment':{'id'}})
@router.get('/get/product/{id:int}/', response_model=productResponse)
async def get_product(id:int=Path(...)):
    product = await ProductsModel.objects.prefetch_related('all_image').get_or_none(id=id, publish=True)

    if product is None:
        return JSONResponse(status_code=404, content='product is not exists')

    return product


@router.get('/all/product/not/publish/', response_model=list[ProductsModel])
async def all_product_not_publish(user:UserSchema=Depends(get_current_user_admin)):
    
    products = await ProductsModel.objects.filter(publish=True).all()

    return products



categorySchema = CategoryModel.get_pydantic(include={'name',})
@router.post('/create/category/', response_model=CategoryModel, response_model_include=['name',])
async def create_category(category:categorySchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')

    category , obj = await CategoryModel.objects.get_or_create(**category.dict())
    
    print(obj)

    if not obj:
        return JSONResponse(status_code=400, content='name is existing')

    return category


commentSchema = CommentsModel.get_pydantic(include={'name','messages'})
@router.post('/create/comment/{product_id:int}', response_model=CommentsModel)
async def create_comment(product_id:int=Path(), comment:commentSchema=Depends()):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')
    
    product = await ProductsModel.objects.get_or_none(id=product_id)

    if product is None:
        return JSONResponse(status_code=404, content='product not found')

    comment = await CommentsModel.objects.create(name=comment.name, messages=comment.messages)

    return comment


productResponse = ProductsModel.get_pydantic(exclude={'category': ..., 'all_comment':...})
@router.post('/create/product/{category_name:str}', response_model=productResponse)
async def create_product(category_name:str=Path(), product:ProductSchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):

    #if not user.get('is_admin'):
    #    return JSONResponse(status_code=203, content='this page for admin')
    category = await CategoryModel.objects.get_or_none(name=category_name)
    if category is None:
        return JSONResponse(status_code=404, content='category doct found')
    
    list_image = str()

    for img in product.image:
        pre, post = img.filename.split('.')
        new_name = f'{pre}-{datetime.now()}.{post}'

        path_save = f"{BASE_DIR}/media/{new_name}"

        with open(path_save, 'wb') as f:
            image = await img.read()
            f.write(image)

        list_image += new_name +','

    product_new = await ProductsModel.objects.create(
        name = product.name,
        description = product.description,
        gender = product.gender,
        attribute = product.attribute,
        number = product.number,
        price = product.price,
        discount = product.discount,
        publish = product.publish,
        images = str(list_image),
        category = category.id,
    )

    return product_new


@router.post('/add/image/{product_id:int}/', response_model=ProductsModel)
async def add_image(product_id:int=Path(...), images:list[UploadFile]=File(...), user:UserSchema=Depends(get_current_user_admin)): 
    #if not user.get('is_admin'):
    #    return JSONResponse(status_code=203, content='this page for admin')
    
    product = await ProductsModel.objects.get_or_none(id=product_id)

    if product is None:
        return JSONResponse(status_code=404, content='product not found')

    list_image = str(product.images).replace('[', '').replace(']', '')
    for img in images:
        pre, post = img.filename.split('.')
        new_name = f'{pre}-{datetime.now()}.{post}'

        path_save = f"{BASE_DIR}/media/{new_name}"

        with open(path_save, 'wb') as f:
            image = await img.read()
            f.write(image)

        list_image += new_name +','
    
    all = '[' + list_image  + ']'
    await product.update(images=all)

    return product


cstegorySchema = CategoryModel.get_pydantic(include={'name'})
@router.put('/update/category/{name:str}/')
async def create_category(name:str=Path(), category:cstegorySchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')
    
    category = await CategoryModel.objects.get(name=name)
    category.name = category.name
    await category.update()

    return category


productResponse = ProductsModel.get_pydantic(exclude={'category':..., 'all_comment':...})
productUpdateSchema = ProductsModel.get_pydantic(exclude={'category':{'id',}, 'created':..., 'images':..., 'all_comment':...})
@router.put('/update/product/', response_model=productResponse)
async def update_product(product:productUpdateSchema=Depends(),user:UserSchema=Depends(get_current_user_admin)):
    obj = await ProductsModel.objects.get_or_none(id=product.id)

    if obj is None:
        return JSONResponse(status_code=404, content='product not found')

    await obj.update(**product.dict())

    return obj


@router.delete('/delete/category/{name:str}/')
async def create_category(user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')

    category = await CategoryModel.objects.get_or_none(name=name)

    if category is None:
        return JSONResponse(status_code=404, content='category is not found')

    await category.all_product.clear(keep_reversed=False)
    await category.delete()

    return JSONResponse(status_code=200, content='category and product related all remove')


@router.delete('/delete/product/{id:int}/')
async def delete_product(id:int=Path(...), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')

    product = await ProductsModel.objects.get_or_none(id=id)
    if product is None:
        return JSONResponse(status_code=404, content='product not found')

    await product.all_comment.clear(keep_reversed=False)
    await product.delete()

    return JSONResponse(status_code=200, content='product delete')


@router.delete('/delete/image/{id:int}/')
async def delete_image(id:int=Path(...), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')

    image = await ImageModel.objects.get_or_none(id=id)
    if image is None:
        return JSONResponse(status_code=404, content='image not found')

    os.remove(os.path.join(BASE_DIR, 'media', str(image.image)))
    await image.delete()
    
    return JSONResponse(status_code=200, content='image deleted')

