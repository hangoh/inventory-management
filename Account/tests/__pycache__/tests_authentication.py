o
    *n�dk  �                   @   s�   d dl mZ d dlmZmZ d dlmZ d dl mZ d dlm	Z	 d dl
mZ d dlmZmZ d dlmZ G d	d
� d
ej�ZG dd� de�ZdS )�    )�authentication)�	MockModel�MockSet)�mock)�
exceptions)�Token)�reverse)�APIRequestFactory�APITestCase)�Userc                   @   s   e Zd ZdZdd� ZdS )�AuthenticationTestZ
Test_Tokenc                 C   s~   |j �d�}|st�d��|�� }|d | jkst|�dkr#t�d��|d }ztjj|d�}|j	}W ||fS    t�d��)	N�AUTHzNo AUTH in headerr   �   zIncorrect Token Format�   )�keyzToken does not exist)
�META�getr   �AuthenticationFailed�split�word�lenr   �objects�user)�self�request�token�http�
auth_tokenZ	token_keyr   � r   �kC:\Users\GohYuHan.AzureAD\mini_project\inventory_management\IM_server\Account\tests\tests_authentication.py�authenticate   s   

�
zAuthenticationTest.authenticateN)�__name__�
__module__�__qualname__r   r    r   r   r   r   r      s    r   c                       sJ   e Zd Ze� Zed�Z� fdd�Zdd� Zdd� Z	dd	� Z
d
d� Z�  ZS )�TestAuthZauthenticateUserc                    sv   t � ��  ttddd�tddd��}tt|jdd�dd�t|jdd�d	d��}t�d
|��� | _t�d|��� | _	d S )Nr   �UncleBen)�id�namer   ZUncleBob)r'   �UncleBen_Key)r   r   ZUncleBob_KeyzAccount.models.User.objectsz-rest_framework.authtoken.models.Token.objects)
�super�setUpr   r   r   r   �patch�startZuser_objects�token_objects)r   �users�keys��	__class__r   r   r*   !   s   


��zTestAuth.setUpc                 C   sJ   | j j| jdd�}t� }|�|| j�\}}| �|jd� | �|jd� d S )NzTest_Token UncleBen_Key�r   r%   r(   )	�factory�post�urlr   r    r-   �assertEqualr'   r   )r   r   �authr   r   r   r   r   �test_auth_success/   s
   zTestAuth.test_auth_successc                 C   �X   | j j| jdd�}t� }| �tj�� |�|| j� W d   � d S 1 s%w   Y  d S )NzTest_Token Uncleben_Keyr2   �	r3   r4   r5   r   �assertRaisesr   r   r    r-   �r   r   r7   r   r   r   �#test_auth_unsuccessfull_wrong_token6   �
   "�z,TestAuth.test_auth_unsuccessfull_wrong_tokenc                 C   r9   )NzToken UncleBen_Keyr2   r:   r<   r   r   r   �*test_auth_unsuccessfull_wrong_token_format<   r>   z3TestAuth.test_auth_unsuccessfull_wrong_token_formatc                 C   sT   | j �| j�}t� }| �tj�� |�|| j� W d   � d S 1 s#w   Y  d S )Nr:   r<   r   r   r   � test_auth_unsuccessfull_no_tokenB   s
   "�z)TestAuth.test_auth_unsuccessfull_no_token)r!   r"   r#   r	   r3   r   r5   r*   r8   r=   r?   r@   �__classcell__r   r   r0   r   r$      s    r$   N)�rest_frameworkr   Zdjango_mock_queries.queryr   r   �unittestr   r   Zrest_framework.authtoken.modelsr   �django.urlsr   Zrest_framework.testr	   r
   ZAccount.modelsr   ZTokenAuthenticationr   r$   r   r   r   r   �<module>   s    