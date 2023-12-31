#!/usr/bin/python3
"""The console for AirBnB clone
"""
import cmd

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    available_classes = [
        "BaseModel",
        "User",
        "Place",
        "State",
        "City",
        "Amenity",
        "Review",
    ]

    def do_quit(self, arg):
        """Exit the console"""
        return True

    def do_EOF(self, arg):
        """Exit the console"""
        return True

    def emptyline(self) -> None:
        pass

    def do_create(self, arg):
        """Creates a new instance of an abject
        Usage:
            $ create <class name>
        """
        if arg is None or arg == "":
            print("** class name missing **")
        else:
            class_name: str = arg.split()[0]
            if class_name not in self.available_classes:
                print("** class doesn't exist **")
            else:
                obj = eval(class_name)()
                obj.save()
                print(f"{obj.id}")

    def do_show(self, arg):
        """Prints an instance of an object
        Usage:
            $ show <class name> <id>
        """
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        elif args[0] not in self.available_classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        for key in all_objs:
            if key.split(".")[0] == args[0] and all_objs[key].id == args[1]:
                print(str(all_objs[key]))
                return
        print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance of an object
        Usage:
            $ destroy <class name> <id>
        """
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        elif args[0] not in self.available_classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        for key in all_objs:
            class_name = all_objs[key].__class__
            if key.split(".")[0] == args[0] and all_objs[key].id == args[1]:
                del all_objs[key]
                storage.save()
                return
        print("** no instance found **")

    def do_all(self, arg):
        """Displays all instances
        Usage:
            $ all
            $ all <class name>
        """
        args = arg.split()
        all_objs = storage.all()
        if len(args) < 1:
            for key in all_objs:
                print(str(all_objs[key]))
            return
        if args[0] not in self.available_classes:
            print("** class doesn't exist **")
            return
        for key in all_objs:
            if key.split(".")[0] == args[0]:
                print(str(all_objs[key]))
        return

    def do_update(self, arg):
        """updates an instance
        Only one attribute can be updated at the time
        Usage:
            update <class name> <id> <attribute name> <attribute value>
        """
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        elif args[0] not in self.available_classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        elif len(args) < 3:
            print("** attribute name missing **")
            return
        elif len(args) < 4:
            print("** value missing **")
            return
        all_objs = storage.all()
        for key in all_objs:
            if (
                key.split(".")[0] == args[0]
                and all_objs[key].id == args[1]
                and args[1] != "created_at"
                and args != "updated_at"
            ):
                obj_key = args[2]
                obj_value = args[3]
                all_objs[key].__dict__[obj_key] = obj_value
                storage.save()
                return
        print("** no instance found **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
