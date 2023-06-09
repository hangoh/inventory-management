o
    v�d  �                   @   sh   d dl mZ d dlmZ d dlmZ d dlmZ d dlm	Z	 d dl
mZ d dlmZ G dd	� d	e�Zd
S )�    )�reverse)�APITestCase)�status)�User)�Store)�Token)�ObjectDoesNotExistc                       s,   e Zd Z� fdd�Zdd� Zdd� Z�  ZS )�UserTestc                    sh   t � ��  tjjdd�}tjjd|d� tjjd|d� tjjdd�}tjjd|d� tjjdd�}d S )	N�UncleBen)�namez
UncleBen'S)�
store_name�userzUncleBen'S_2ZUncleBobz
UncleBob'SZUncleBam)�super�setUpr   �objects�creater   )�selfr   Zuser2Zuser3��	__class__� �aC:\Users\GohYuHan.AzureAD\mini_project\inventory_management\IM_server\Account\tests\tests_view.pyr   
   s   
zUserTest.setUpc                 C   s`   t d�}ddi}| jj||dd�}| �|jtj� | �tjj	|j
�	d�d�jtjj	dd	�� d S )
N�authenticateUser�usernamer
   �json��formatr   )�key�   )�id)r   �client�post�assertEqual�status_coder   ZHTTP_200_OKr   r   �get�datar   r   �r   �urlr$   �responser   r   r   �test_authenticateUser_success   s
   .z&UserTest.test_authenticateUser_successc                 C   s.   t d�}ddi}| jj||dd�}t|� d S )Nr   r   ZUnclebenr   r   )r   r   r    �printr%   r   r   r   �test_authenticateUser_fail    s   z#UserTest.test_authenticateUser_fail)�__name__�
__module__�__qualname__r   r(   r*   �__classcell__r   r   r   r   r	   	   s    r	   N)�django.urlsr   Zrest_framework.testr   �rest_frameworkr   ZAccount.modelsr   ZMaterial.modelsr   Zrest_framework.authtoken.modelsr   �django.core.exceptionsr   r	   r   r   r   r   �<module>   s    