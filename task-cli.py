import os
import sys 
import json
import datetime


class TaskHandler:
    
    def __init__(self,path):
        self.path = path
        self.d = []
        with open(self.path, 'r', encoding='utf-8') as file:
            try:
                self.d = json.load(file)
                if not isinstance(self.d, list):
                    self.d = []
            except json.JSONDecodeError:
                pass
        

    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def write(self):
        # Write the updated list back to the file (overwrite)
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(self.d, file, indent=2)
   
    # add
    def add(self,task):
    
        # compute new id
        new_id = 1
        if self.d:
            try:
                last_id = int(self.d[-1].get('id', 0))
                new_id = last_id + 1
            except Exception:
                # fallback: find max id
                new_id = max((int(item.get('id', 0)) for item in self.d), default=0) + 1

        curTask = {
            "id": new_id,
            "description": task,
            "status": "todo",
            "createdAt": self.now(),
            "updatedAt": self.now()
        }

        self.d.append(curTask)
        self.write()
        print(f"Added task id={new_id}")
        
                
             
    # update
    def update(self,taskId,task):
        found = False
        for item in self.d:
            if str(item.get('id')) == str(taskId):
                item['description'] = task
                item['updatedAt'] = self.now()
                found = True
                break
        if found:
            self.write()
            print(f"Updated task id={taskId}")
        else:
            print(f"Task id={taskId} not found.")
    # delete
    def delete(self,taskId):
        initial_length = len(self.d)
        self.d = [item for item in self.d if str(item.get('id')) != str(taskId)]
        if len(self.d) < initial_length:
            self.write()
            print(f"Deleted task id={taskId}")
        else:
            print(f"Task id={taskId} not found.")
    # list all
    def listAll(self):
        if len(self.d) == 0:
            print("No tasks found.")
            return
        # Header: ID, Created At, Updated At, Status, Description
        print("ID \t Created At \t\t Updated At \t\t Status \t Description")
        for item in self.d:
            # Print columns in the order: ID, Created At, Updated At, Status, Description
            print(item.get('id'), "\t", item.get('createdAt'), "\t", item.get('updatedAt'), "\t", item.get('status'), "\t\t", item.get('description'))
    # list done
    def listDone(self):
        if len(self.d) == 0:
            print("No tasks found.")
            return
        # Header: ID, Created At, Updated At, Status, Description
        print("ID \t Created At \t\t Updated At \t\t Status \t Description")
        for item in self.d:
            if item.get('status') == 'done':
                print(item.get('id'), "\t", item.get('createdAt'), "\t", item.get('updatedAt'), "\t", item.get('status'), "\t\t", item.get('description'))  
 
    # like not done
    def listNotDone(self):
        if len(self.d) == 0:
            print("No tasks found.")
            return
        # Header: ID, Created At, Updated At, Status, Description
        print("ID \t Created At \t\t Updated At \t\t Status \t Description")
        for item in self.d:
            if item.get('status') == 'todo':
                print(item.get('id'), "\t", item.get('createdAt'), "\t", item.get('updatedAt'), "\t", item.get('status'), "\t\t", item.get('description'))
   
    # list in progress
    def listInProgress(self):
        if len(self.d) == 0:
            print("No tasks found.")
            return
        # Header: ID, Created At, Updated At, Status, Description
        print("ID \t Created At \t\t Updated At \t\t Status \t Description")
        for item in self.d:
            if item.get('status') == 'in-progress':
                print(item.get('id'), "\t", item.get('createdAt'), "\t", item.get('updatedAt'), "\t", item.get('status'), "\t\t", item.get('description'))
    # mark in progress
    def markInProgress(self,taskId):
        found = False
        for item in self.d:
            if str(item.get('id')) == str(taskId):
                item['status'] = 'in-progress'
                item['updatedAt'] = self.now()
                found = True
                break
        if found:
            self.write()
            print(f"Marked task id={taskId} as in-progress")
        else:
            print(f"Task id={taskId} not found.")
    # mark done
    def markDone(self,taskId):
        found = False
        for item in self.d:
            if str(item.get('id')) == str(taskId):
                item['status'] = 'done'
                item['updatedAt'] = self.now()
                found = True
                break
        if found:
            self.write()
            print(f"Marked task id={taskId} as done")
        else:
            print(f"Task id={taskId} not found.")

def start(args):
    # print(args) 
    path = "./data.json"
   
    if not os.path.isfile(path):
        with open(path,'w') as file:
            pass 
    if len(args) >1:
        TH = TaskHandler(path) 
        if args[1] == "add":
            TH.add(args[2])
        elif args[1] == "update":
            TH.update(args[2], args[3])
        elif args[1] == "delete":
            TH.delete(args[2])
        elif args[1] == "list":
            TH.listAll()
        elif args[1] == "done":
            TH.listDone()
        elif args[1] == "todo":
            TH.listNotDone()
        elif args[1] == "in-progress":
            TH.listInProgress()
        elif args[1] == "mark-in-progress":
            TH.markInProgress(args[2])
        elif args[1] == "mark-done":
            TH.markDone(args[2])
        else:
            print("Unknown command")


if __name__ == "__main__":
    start(sys.argv)



