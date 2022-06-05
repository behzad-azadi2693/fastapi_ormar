from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from .models import BasketModel, OrdersModel, AddressModel
from accounts.utils import get_current_user
from accounts.schema import UserSchema
from .response import BasketResponse, MyBasketResponse
from products.models import ProductsModel
from .schema import AddressSchema


router = APIRouter(prefix='/carts', tags=['cart'])


@router.get('/all/baskets/', response_model=list[BasketResponse])
async def all_baskets(user:UserSchema=Depends(get_current_user)):
    bskets = await BasketModel.objects.filter(user__id=user.get('id'))

    return basket


@router.get('/my/basket/{id:int}', response_model=MyBasketResponse)
async def my_basket(id:int=Path(...), user:UserSchema=Depends(get_current_user)):
    basket = await BasketModel.objects.prefech_related('basket_orders').get_or_one(id=id, user__id = user.get('id'))

    if basket is None:
        return JSONResponse(status_code=404, content='basket dos not exists')

    return basket



@router.post('/add/prudoct/{product_id:int}/')
async def add_product(product_id:int=Path(...), user:UserSchema=Depends(get_current_user)):
    product = await ProductsModel.objects.get_or_none(id = product_id, number__ge=1)

    if product is None:
        return JSONResponse(status_code=404, content='dos not exits product')

    basket, obj = await BasketModel.objects.get_or_create(user__id=user.get('id'), payed=False)

    order, check = await  OrdersModel.objects.get_or_create(basket=basket, product=product)

    if check:
        return JSONResponse(status_code=201, content='produt add to basket')
    else:
        return JSONResponse(status_code=200, content='produt is exists in basket')


@router.post('/add/address/')
async def add_address(user:UserSchema=Depends(get_current_user), address:AddressSchema=Depends()):
    basket = await BasketModel.objects.get_or_none(user__id=user.get('id'), payed=False)

    if basket is None:
        return JSONResponse(status_code=404, content='basket not found')

    address_new, check = await AddressModel.objects.update_or_create(basket=basket,
                                name = address.name, phone = address.phone ,address = address.address)


@router.put('/increase/number/order/{order_id:int}/')
async def incress_number_order(user:UserSchema=Depends(get_current_user), order_id:int=Path(...)):
    order = await OrdersModel.objects.get_or_none(
        basket__user__id = user.get('id'),
        basket__payed = False,
        number__lt = product__number,
    )

    if order is None:
        return JSONResponse(status_code=404, content='order don found')

    order.number += 1
    await order.update()

    return JSONResponse(status_code=200, content='number addedd one')


@router.put('/decrease/number/order/{order_id:int}/')
async def decrease_number_order(user:UserSchema=Depends(get_current_user), order_id:int=Path(...)):
    order = await OrdersModel.objects.get_or_none(
        basket__user__id = user.get('id'),
        basket__payed = False,
        number__ge = 1,
    )

    if order is None:
        return JSONResponse(status_code=404, content='order don found')

    order.number -= 1
    await order.update()

    return JSONResponse(status_code=200, content='number addedd one')



@router.delete('/remove/basket/')
async def delete_basket(user:UserSchema=Depends(get_current_user)):
    basket = await BasketModel.objects.get_or_none(user__id=user.get('id'), payed=False)

    if basket is None:
        return JSONResponse(status_code=404, content='basket dos not exists')

    await basket.basket_orders.clear(keep_reversed=False)
    await basket.delete()

    return JSONResponse(status_code=200, content='basket is deleted')



@router.delete('/remove/orders/{orders_id:int}')
async def remove_orders(user:UserSchema=Depends(get_current_user), orders_id:int=Path(...)):
    basket = await BasketModel.objects.get_or_none(user_id=user.get('id'), payed=False)
    
    if basket is None:
        return JSONResponse(status_code=400, content='basket not found')

    order = await OrdersModel.objects.get_or_none(basket=basket, id=orders_id)

    if order is None:
        return JSONResponse(status_code=404, content='order is not found')

    await order.delete()

    return JSONResponse(status_code=200, content='order is deleted')