package mrf.camera2api.testapp;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageButton;


public class Gallery extends AppCompatActivity {
    private ImageButton mBtGoBack;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gallery);
        mBtGoBack = (ImageButton) findViewById(R.id.btn_Camera);
        mBtGoBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                finish();
            }
        });
//        RecyclerView recyclerView = (RecyclerView)findViewById(R.id.imagegallery);
//        recyclerView.setHasFixedSize(true);
//
//        RecyclerView.LayoutManager layoutManager = new GridLayoutManager(getApplicationContext(),2);
//        recyclerView.setLayoutManager(layoutManager);
//        ArrayList<CreateList> createLists = prepareData();
//        MyAdapter adapter = new MyAdapter(getApplicationContext(), createLists);
//        recyclerView.setAdapter(adapter);
    }
//    private ArrayList<CreateList> prepareData(){
//
//        ArrayList<CreateList> theimage = new ArrayList<>();
//        for(int i = 0; i< image_titles.length; i++){
//            CreateList createList = new CreateList();
//            createList.setImage_title(image_titles[i]);
//            createList.setImage_ID(image_ids[i]);
//            theimage.add(createList);
//        }
//        return theimage;
//    }
}
