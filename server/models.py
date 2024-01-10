from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class MyValidator:
    def stringHasAtLeastOrAtMostXChars(self, key, val, minnumchars = 1,
                                       useatmost = False, nm = "", item = ""):
        if (type(minnumchars) == int): pass;
        else: raise ValueError("minnumchars must be an integer!");
        if (nm == None or type(nm) != str or len(nm) < 1):
            raise ValueError("name parameter must not be empty!");
        if (item == None or type(item) != str or len(item) < 1):
            raise ValueError("item parameter must not be empty!");
        if (type(val) == str):
            #at most
            if (useatmost): 
                if (len(val) < minnumchars + 1): return val;
                else: raise ValueError(f"all {nm}s must have a {item}!");
            else:
                #at least
                if (len(val) < minnumchars): raise ValueError(f"all {nm}s must have a {item}!");
                else: return val;
        else: raise ValueError(f"the {nm}'s {item} must be a string!");

    def stringHasAtLeastXChars(self, key, val, minnumchars = 1, nm = "", item = ""):
        return self.stringHasAtLeastOrAtMostXChars(key, val, minnumchars, False, nm, item);

    def stringHasAtMostXChars(self, key, val, maxnumcharsex = 1, nm = "", item = ""):
        return self.stringHasAtLeastOrAtMostXChars(key, val, maxnumcharsex, True, nm, item);

    def stringIsNotEmpty(self, key, val, nm = "", item = ""):
        return self.stringHasAtLeastXChars(key, val, 1, nm, item);

mv = MyValidator();

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    #author names are unique and all authors have names
    @validates("name")
    def nameisvalid(self, key, val):
        retval = mv.stringIsNotEmpty(key, val, "author", "name");
        #print(f"retval = {retval}");
        #print(f"val = {val}");
        #print(Author.query.all());
        anames = [a.name for a in Author.query.all()];
        for nm in anames:
        #    print(f"nm = {nm}");
        #    print(f"val = {val}");
            if (nm == val): raise ValueError("duplicate name found!");
        return retval;
        #if (type(val) == str):
        #    if (len(val) < 1): raise ValueError("all authors must have a name!");
        #    else: return val;
        #else: raise ValueError("the author's name must be a string!");

    @validates("phone_number")
    def phonenumberisvalid(self, key, val):
        if (type(val) == str):
            if (len(val) == 10):
                for c in val:
                    throwex = False;
                    try:
                        a = int(c);
                    except Exception as err:
                        throwex = True;
                    
                    if (throwex):
                        raise ValueError("all phone numbers must have 10 digits and no " +
                                         "other characters!");
                return val;
            else: raise ValueError("all phone numbers must have 10 digits!");
        else: raise ValueError("the phone number must be a string!");

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def titleisvalid(self, key, val):
        retval = mv.stringIsNotEmpty(key, val, "post", "title");
        mysstrs = ["Won't Believe", "Secret", "Top", "Guess"];
        for mstr in mysstrs:
            if (mstr in retval): return retval;
        raise ValueError(f"all posts must have a title that contains one of the following {mysstrs}!");
        #if (type(val) == str):
        #    if (len(val) < 1): raise ValueError("all posts must have a title!");
        #    else: return val;
        #else: raise ValueError("the post's title must be a string!");

    @validates("content")
    def contentisvalid(self, key, val):
        return mv.stringHasAtLeastXChars(key, val, 250, "post", "content");

    @validates("summary")
    def summaryisvalid(self, key, val):
        return mv.stringHasAtMostXChars(key, val, 250, "post", "summary");

    @validates("category")
    def categoryisvalid(self, key, val):
        if (val not in ["Fiction", "Non-Fiction"]):
            raise ValueError("all categories must be either Fiction or Non-Fiction!");
        else: return val;

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
