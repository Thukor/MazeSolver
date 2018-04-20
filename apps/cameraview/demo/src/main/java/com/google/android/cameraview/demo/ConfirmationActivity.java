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

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import java.io.File;
import java.io.FileFilter;
import java.io.FileOutputStream;
import java.io.IOException;

public class ConfirmationActivity extends AppCompatActivity {
    @Override

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_confirmation);

        File imgDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        final File imgFile = lastFileModified(imgDir.toString());

        if (imgFile.exists()) {
            Matrix matrix = new Matrix();
            matrix.postRotate(90);

            Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
            Bitmap rotatedBitmap = Bitmap.createBitmap(myBitmap, 0, 0, myBitmap.getWidth(),
                    myBitmap.getHeight(), matrix, true);
            ImageView myImage = (ImageView) findViewById(R.id.imgView);

            myImage.setImageBitmap(rotatedBitmap);

        }
        Button goBack = (Button) findViewById(R.id.back);
        assert goBack != null;
        goBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

        Button solveMaze = (Button) findViewById(R.id.solve);
        assert solveMaze != null;
        solveMaze.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new ServerConnection().execute(imgFile);

            }
        });
    }

    /**
     * Async task runs the connector in the background so the current view can be separated from
     * the operation
     */
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
        protected void onPostExecute(String result) {
            launchSolutionViewActivity();
        }
    }

    /**
     * sends us to the solution view activity
     */
    private void launchSolutionViewActivity() {
        startActivity(new Intent(this, SolutionViewActivity.class));
    }

    /**
     * @param dir
     * @return last modified file in the directory. This will be the most recent taken image
     */
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

    /**
     *
     * @param bytes
     * @effects decodes a string of bytes that was encoded into Base64 format. Decoding the string
     *          gives us the digital image
     * @throws Exception
     */
    private void bytesToImage(String bytes) throws Exception {
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
