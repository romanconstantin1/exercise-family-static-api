
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # example list of members
        self._members = [
            {
                "id": self._generateId(),
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generateId(),
                "first_name": "Jane",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generateId(),
                "first_name": "Jimmy",
                "last_name": last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def get_member(self, id):
        member = list(filter(lambda sub: sub["id"] in [id], self._members))
        if len(member) == 0:
            member.append({"not_found": True})
            return member
        return member

    def add_member(self, member):
        required_params = {"id", "first_name", "age", "lucky_numbers"}
        if not member.keys() >= required_params:
            return {"missing_params": True}

        new_member = {
            "id": member["id"],
            "first_name": member["first_name"],
            "last_name": self.last_name,
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
        self._members.append(new_member)
        return new_member

    def delete_member(self, id):
        for i in range(len(self._members)):
            if self._members[i]["id"] == id:
                to_delete = self._members[i]
                del self._members[i]
                to_delete["done"] = True
                return to_delete
        return {"not_found": True}

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        print(self._members)
        return self._members
