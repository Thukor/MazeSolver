/*
 * Copyright (C) 2016 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.google.android.cameraview.demo;

import static android.util.Base64.DEFAULT;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;
import java.io.FileFilter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

public class GalleryActivity extends AppCompatActivity {
    private Vector<ImageView> mySDCardImages= new Vector<ImageView>();
    private Integer[] mThumbIds = null;
    File[] sdDirFiles = null;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gallery);

        loadImages();

        GridView gridview = (GridView) findViewById(R.id.gridview);
        gridview.setAdapter(new ImageAdapter(this));

        Button goBack = (Button) findViewById(R.id.back);
        assert goBack != null;
        goBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

        gridview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View v, int position, long id) {
                File toSend = sdDirFiles[position];
                new ServerConnection().execute(toSend);
            }
        });
    }

    public void loadImages(){
        List<Integer> drawablesId = new ArrayList<Integer>();
        int picIndex=12345;
        File sdDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        sdDirFiles = sdDir.listFiles();
        for(File singleFile : sdDirFiles)
        {
            if (!singleFile.getName().contains("solution")){
                ImageView myImageView = new ImageView(this);
                myImageView.setImageDrawable(Drawable.createFromPath(singleFile.getAbsolutePath()));
                myImageView.setId(picIndex);
                picIndex++;
                drawablesId.add(myImageView.getId());
                mySDCardImages.add(myImageView);
            }
        }
        mThumbIds = (Integer[])drawablesId.toArray(new Integer[0]);
    }


    public class ImageAdapter extends BaseAdapter {
        private Context mContext;

        public ImageAdapter(Context c) {
            mContext = c;
        }

        public int getCount() {
            return mySDCardImages.size();
        }

        public Object getItem(int position) {
            return null;
        }

        public long getItemId(int position) {
            return 0;
        }


        // create a new ImageView for each item referenced by the Adapter
        public View getView(int position, View convertView, ViewGroup parent) {
            ImageView imageView;
            if (convertView == null) {
                // if it's not recycled, initialize some attributes
                imageView = new ImageView(mContext);
                imageView.setLayoutParams(new ViewGroup.LayoutParams(250, 250));
                imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
                imageView.setPadding(8, 8, 8, 8);
            } else {
                imageView = (ImageView) convertView;
            }

            imageView.setImageDrawable(mySDCardImages.get(position).getDrawable());
            return imageView;
        }


    }

    class ServerConnection extends AsyncTask<File, Void, String> {
        @Override
        protected String doInBackground(File... file) {
            String solutionFile = null;
            try {

                HttpURLConnector http = new HttpURLConnector();
                String urlParameter = http.imageToBytes(file[0]);
                System.out.println("hello friend " + urlParameter);
                solutionFile = http.sendPost(urlParameter);
                bytesToImage(solutionFile);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(String result){
            launchSolutionViewActivity();
        }
    }
    private void launchSolutionViewActivity() {
        startActivity(new Intent(this, SolutionViewActivity.class));
    }

    private void bytesToImage(String bytes) throws Exception
    {
        String fileName = "solution.jpg";
        System.out.println(bytes.length());
        File file = new File(getExternalFilesDir(Environment.DIRECTORY_PICTURES), fileName);
        try {
            FileOutputStream fos = new FileOutputStream(file);
            byte byteArray[] = Base64.decode(bytes, DEFAULT);
            fos.write(byteArray);
            fos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


