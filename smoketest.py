import requests
from datetime import date


def run_smoketest():
    base_url = "http://localhost:5000/api"
    username = "test"
    password = "test"


    order_wilson = {
        "order_id": 1,
        "customer": "Alex",
        "stringer": "Alex",
        "order_date": date(2025, 6, 10),
        "racket": "Wilson Pro Staff",
        "mains_tension": 52,
        "mains_string": "Luxilon ALU Power",
        "crosses_tension": 52,
        "crosses_string": "Luxilon ALU Power",
        "replacement_grip": None,
        "paid": False,
        "completed": False
    }

    order_head = {
        "order_id": 2,
        "customer": "Rocky",
        "stringer": "Alex",
        "order_date": date(2025, 6, 18),
        "racket": "Head Speed MP",
        "mains_tension": 54,
        "mains_string": "Head Velocity",
        "crosses_tension": 50,
        "crosses_string": "Head Synthetic Gut",
        "replacement_grip": "Head White Tacky",
        "paid": True,
        "completed": True
    }

    updated_wilson = {
        "customer": "Alex",
        "order_date": date(2025, 6, 10),
        "racket": "Wilson Pro Staff",
        "mains_tension": 52,
        "mains_string": "Luxilon ALU Power",
        "crosses_tension": 50,
        "crosses_string": "Wilson Sensation",
        "replacement_grip": None
    }

    health_response = requests.get(f"{base_url}/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "success"

    reset_users_response = requests.delete(f"{base_url}/reset-users")
    assert reset_users_response.status_code == 200
    assert reset_users_response.json()["status"] == "success"
    print("Reset users successful")

    reset_orders_response = requests.delete(f"{base_url}/reset-orders")
    assert reset_orders_response.status_code == 200
    assert reset_orders_response.json()["status"] == "success"
    print("Reset orders successful")

    create_user_response = requests.put(f"{base_url}/create-user", json={
        "username": username,
        "password": password
    })
    assert create_user_response.status_code == 201
    assert create_user_response.json()["status"] == "success"
    print("User creation successful")

    session = requests.Session()

#     # Log in
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": password
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["status"] == "success"
    print("Login successful")

    wilson_id = 1
    create_wilson_resp = session.post(f"{base_url}/create-order", json=order_wilson)
    assert create_wilson_resp.status_code == 201
    assert create_wilson_resp.json()["status"] == "success"
    print("Order creation successful")

#     # Change password
    change_password_resp = session.post(f"{base_url}/change-password", json={
        "new_password": "new_password"
    })
    assert change_password_resp.status_code == 200
    assert change_password_resp.json()["status"] == "success"
    print("Password change successful")

#     # Log in with new password
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": "new_password"
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["status"] == "success"
    print("Login with new password successful")


    head_id = 2
    create_head_resp = session.post(f"{base_url}/create-order", json=order_head)
    assert create_head_resp.status_code == 201
    assert create_head_resp.json()["status"] == "success"
    print("Order creation successful")


    get_order_by_id_resp = session.get(f"{base_url}/get-order-from-history-by-id/{wilson_id}")
    assert get_order_by_id_resp.status_code == 200
    assert get_order_by_id_resp.json()["customer"] == "Alex"
    assert get_order_by_id_resp.json()["status"] == "success"
    print("order retrieved successfully")


#     add_order_to_plan_resp = session.post(f"{base_url}/add-order-to-plan/{biceps_id}")
#     assert add_order_to_plan_resp.status_code == 200
#     assert add_order_to_plan_resp.json()["status"] == "success"
#     assert add_order_to_plan_resp.json()["message"] == "order biceps - 35.0 out of 40 added to plan"
#     print("order added to plan successfully")


#     get_rec_resp = session.get(f"{base_url}/orders/recommendations/{pecs_id}")
#     assert get_rec_resp.status_code == 200
#     assert get_rec_resp.json()["status"] == "success"
#     assert get_rec_resp.json()["recommendations"] == [{'bodyPart': 'chest', 'equipment': 'leverage machine', 'gifUrl': 'https://v2.exercisedb.io/image/M1vEH1gTLk2nxf', 'id': '0009', 'name': 'assisted chest dip (kneeling)', 'target': 'pectorals', 'secondaryMuscles': ['triceps', 'shoulders'], 'instructions': ['Adjust the machine to your desired height and secure your knees on the pad.', 'Grasp the handles with your palms facing down and your arms fully extended.', 'Lower your body by bending your elbows until your upper arms are parallel to the floor.', 'Pause for a moment, then push yourself back up to the starting position.', 'Repeat for the desired number of repetitions.']}]
#     print("recommendation retrieved successfully")

#     log_workout_resp = session.post(f"{base_url}/orders/log-session/{pecs_id}", json=example_workout)
#     assert log_workout_resp.status_code == 200
#     assert log_workout_resp.json()["status"] == "success"
#     assert log_workout_resp.json()["message"] == "order completed! Total progress: 125.0%"
#     print("workout logged successfully")


    # get_all_orders_from_plan_resp = session.get(f"{base_url}/get-all-orders-from-plan")
    # assert get_all_orders_from_plan_resp.status_code == 200
    # assert get_all_orders_from_plan_resp.json()["status"] == "success"
    # assert get_all_orders_from_plan_resp.json()["orders"] == [biceps_id]
    # print("plan retrieved successfully")


#     get_plan_progress_resp = session.get(f"{base_url}/get-plan-progress")
#     assert get_plan_progress_resp.status_code == 200
#     assert get_plan_progress_resp.json()["status"] == "success"
#     assert get_plan_progress_resp.json()["percentage"] == 0.0
#     print("plan progress retrieved successfully")


#     remove_order_from_plan_resp = session.delete(f"{base_url}/remove-order-from-plan/{biceps_id}")
#     assert remove_order_from_plan_resp.status_code == 200
#     assert remove_order_from_plan_resp.json()["status"] == "success"
#     assert remove_order_from_plan_resp.json()["message"] == f"order with id {biceps_id} removed from plan"
#     print("order removed from plan successfully")


#     clear_plan_resp = session.post(f"{base_url}/clear-plan")
#     assert clear_plan_resp.status_code == 200
#     assert clear_plan_resp.json()["status"] == "success"
#     print("plan cleared successfully")

    get_order_by_customer_resp = session.get(f"{base_url}/orders/by-customer/{order_wilson["customer"]}")
    assert get_order_by_customer_resp.status_code == 200
    assert get_order_by_customer_resp.json()["orders"] == [wilson_id]
    assert get_order_by_customer_resp.json()["status"] == "success"
    print("Order retrieved successfully - customer")


    get_order_by_completed_resp = session.get(f"{base_url}/orders/by-completed/{order_head["completed"]}")
    assert get_order_by_completed_resp.status_code == 200
    assert get_order_by_completed_resp.json()["orders"] == [head_id]
    assert get_order_by_completed_resp.json()["status"] == "success"
    print("Order retrieved successfully - completed")


    get_order_by_date_resp = session.get(f"{base_url}/orders/by-date/{order_wilson["order_date"]}")
    assert get_order_by_date_resp.status_code == 200
    assert get_order_by_date_resp.json()["orders"] == [wilson_id]
    assert get_order_by_date_resp.json()["status"] == "success"
    print("Order retrieved successfully - date")


    update_order_resp = session.patch(f"{base_url}/update-order/{wilson_id}", json=updated_wilson)
    assert update_order_resp.status_code == 200
    assert update_order_resp.json()["status"] == "success"
    assert update_order_resp.json()["updated_fields"] == [updated_wilson["crosses_tension"], updated_wilson["crosses_string"]]
    print("Order updated successfully")

    
    get_all_orders_resp = session.get(f"{base_url}/get-all-orders-from-history")
    assert get_all_orders_resp.status_code == 200
    assert [get_all_orders_resp.json()["orders"][0]["id"],get_all_orders_resp.json()["orders"][1]["order_id"]] == [wilson_id, head_id]
    assert get_all_orders_resp.json()["status"] == "success"
    print("Orders retrieved successfully")


    delete_head_resp = session.delete(f"{base_url}/delete-order/{head_id}")
    assert delete_head_resp.status_code == 200
    assert delete_head_resp.json()["status"] == "success"
    print("order deletion successful")


    fake_id = 3
    delete_fake_resp = session.delete(f"{base_url}/delete-order/{fake_id}")
    assert delete_fake_resp.status_code == 500
    assert delete_fake_resp.json()["status"] == "error"
    print("order deletion failed as expected")

#     # Log out
    logout_resp = session.post(f"{base_url}/logout")
    assert logout_resp.status_code == 200
    assert logout_resp.json()["status"] == "success"
    print("Logout successful")

    create_boxer_logged_out_resp = session.post(f"{base_url}/create-order", json=order_head)
    # This should fail because we are logged out
    assert create_boxer_logged_out_resp.status_code == 401
    assert create_boxer_logged_out_resp.json()["status"] == "error"
    print("order creation failed as expected")

if __name__ == "__main__":
    run_smoketest()