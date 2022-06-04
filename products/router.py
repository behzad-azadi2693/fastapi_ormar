from fastapi import  APIRouter, Depends, Path, status, Body, File, UploadFile
from accounts.utils import get_current_user_admin, get_current_user
from .schema import CategorySchema, ProductSchema, ProductUpdateSchema, CommentSchema
from .models import CategoryModel, ProductsModel, ImageModel, CommentsModel
from .response import CategoryResponse, ProductResponse, CommentResponse, CategoryProductResponse
from fastapi.responses import JSONResponse
from config.settings import BASE_DIR
from datetime import datetime
from accounts.schema import UserSchema
import os


router = APIRouter(prefix='/product', tags=['produucts'])


@router.get('/all/ctegories/', response_model=list[CategorySchema])
async def all_category():
    categories = await CategoryModel.objects.all()
    return categories


@router.get('/get/category/{name:str}/', response_model=CategoryResponse)
async def get_category(name:str=Path(...)):
    category = await CategoryModel.objects.prefech_related('all_product').get(name=name)

    if not category:
        return JSONResponse(status_code = 404, content='nothing found enything')

    return category


@router.get('/get/product/{id:int}/', response_model=ProductResponse)
async def get_product(id:int=Path(...)):
    product = await ProductsModel.objects.prefetch_related('all_image', 'all_comment').get(id=id, publish=True)

    return product


@router.get('/all/product/not/publish/', response_model=list[CategoryProductResponse])
async def all_product_not_publish(user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')

    products = await ProductsModel.objects.filter(publidh=False)

    return products 


@router.post('/create/category/')
async def create_category(name:CategorySchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')
    
    category = await CategoryModel.objects.create(name=category.name)

    return category


@router.post('/create/product/{id:int}/', response_model=ProductResponse)
async def create_product(id:int=Path(...), product:ProductSchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')
    
    category = await CategoryModel.objects.get_or_none(id=id)
    if category is None:
        return JSONResponse(status_code=404, content='category doct found')

    product_new = await ProductsModel.objects.create(
        name = product.name,
        description = product.description,
        attribute = product.attribute,
        gender = product.gender,
        number = product.number,
        price = product.price,
        discount = product.discount,
        publish = product.publish,
        category = category,
    )

    for img in product.image:
        pre, post = img.filename.split('.')
        new_name = f'{pre}-{datetime.now()}.{post}'

        path_save = f"{BASE_DIR}/media/{new_name}"

        with open(path_save, 'wb') as f:
            image = await img.read()
            f.write(image)
        
        await ImageModel.objects.create(image=new_name, product=product_new)

    return product_new


@router.post('/add/image/{product_id:int}/')
async def add_image(id:int=Path(...), image:list[UploadFile]=File(...), user:UserSchema=Depends(get_current_user_admin)): 
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')
    
    product = await ProductsModel.objects.get_or_none(id=product_id)

    if product is None:
        return JSONResponse(status_code=404, content='product not found')

    for img in image:
        pre, post = img.filename.split('.')
        new_name = f'{pre}-{datetime.now()}.{post}'

        path_save = f"{BASE_DIR}/media/{new_name}"

        with open(path_save, 'wb') as f:
            image = await img.read()
            f.write(image)
        
        await ImageModel.objects.create(image=new_name, product=product_new)

    return JSONResponse(status_code=201, content='image all added')


@router.post('/create/comment/{product_id:int}/', response_model=CommentResponse)
async def create_comment(id:int=Path(...), comment:CommentSchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')
    
    product = await ProductsModel.objects.get_or_none(id=product_id)

    if product is None:
        return JSONResponse(status_code=404, content='product not found')

    comment = await CommentsModel.objects.create(name=comment.name, messages=comment.messages)

    return comment


@router.put('/update/category/{name:str}/')
async def create_category(category:CategorySchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')
    
    category = await CategoryModel.objects.get(name=name)
    category.name = category.name
    await category.update()

    return category


@router.put('/update/product/{id:int}/')
async def update_product(id:int=Path(...), product:ProductUpdateSchema=Depends(), user:UserSchema=Depends(get_current_user_admin)):
    obj = await ProductsModel.objects.get(id=id)
    obj.name = product.name,
    obj.description = product.description,
    obj.attribute = product.attribute,
    obj.gender = product.gender,
    obj.number = product.number,
    obj.price = product.price,
    obj.discount = product.discount,
    obj.publish = product.publish,
    obj.category = category,
    await opj.update()

    return obj


@router.delete('/delete/category/{name:str}/')
async def create_category(user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')

    category = await CategoryModel.objects.get_or_none(name=name)

    if category is None:
        return JSONResponse(status_code=404, content='category is not found')

    category.all_product.clear(keep_reversed=False)
    await category.delete()

    return JSONResponse(status_code=200, content='category and product related all remove')


@router.delete('/delete/product/{id:int}/')
async def delete_product(id:int=Path(...), user:UserSchema=Depends(get_current_user_admin)):
    if not user.get('is_admin'):
        return JSONResponse(status_code=203, content='this page for admin')

    product = await ProductsModel.objects.get_or_none(id=id)
    if product is None:
        return JSONResponse(status_code=404, content='product not found')

    await product.all_image.clear(keep_reversed=False)
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


#prefetch related for publish True