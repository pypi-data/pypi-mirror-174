from PIL import Image
def file_ext_change(path,new_ext):
    image=Image.open(path)
    new_path=path[:len(path)-3]+str(new_ext)
    image.save(new_path)
    return new_path

def file_name_change(path,new_name):
    image=Image.open(path)
    new_image=new_name+str(path[len(path)-4:])
    image.save(new_image)
    return new_image
