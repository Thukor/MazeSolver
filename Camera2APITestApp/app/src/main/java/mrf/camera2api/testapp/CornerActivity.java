package mrf.camera2api.testapp;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import java.io.File;
import java.io.FileFilter;

public class CornerActivity extends AppCompatActivity {
    private Button goBack;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_corner);
        File imgDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM);
        File mImageFolder = new File(imgDir, "MazeSolver");
        File imgFile = lastFileModified(mImageFolder.toString());

//        File mImageChild = new File(mImageFolder,"kms.jpg");
//        File imgFile = new  File("/zz/Images/test_image.jpg");

        if(imgFile.exists()){
            Matrix matrix = new Matrix();
            matrix.postRotate(90);

            Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
            Bitmap rotatedBitmap = Bitmap.createBitmap(myBitmap, 0, 0, myBitmap.getWidth(),       myBitmap.getHeight(), matrix, true);
            ImageView myImage = (ImageView) findViewById(R.id.imgView);

            myImage.setImageBitmap(rotatedBitmap);

        }
        goBack = (Button) findViewById(R.id.back);
        assert goBack != null;
        goBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                finish();
            }
        });
    }
    public static File lastFileModified(String dir) {
        File fl = new File(dir);
        File[] files = fl.listFiles(new FileFilter() {
            public boolean accept(File file) {
                return file.isFile();
            }
        });
        long lastMod = Long.MIN_VALUE;
        File choice = null;
        for (File file : files) {
            if (file.lastModified() > lastMod) {
                choice = file;
                lastMod = file.lastModified();
            }
        }
        return choice;
    }
}
