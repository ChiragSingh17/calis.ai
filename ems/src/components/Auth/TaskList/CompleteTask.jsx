import React from 'react'
 const CompleteTask = ({data}) =>{
  return(
    <div className='h-full flex-shrink-0 w-[300px] p-5 bg-green-400 rounded-xl'>
            <div className='flex justify-between items-center'>
              <h3 className='bg-red-600 px-3 py-1 rounded'>{data.category}</h3>
              <h4>{data.date}</h4>
           </div>
           <h2 className='mt-5 text-xl font-semibold'>{data.title}</h2>
           <div className='mt-2'>
            <p>
              {data.description}
            </p>
                <button className=' mt-3 w-full bg-blue-600'>Complete</button>
           </div>
        </div>
  )
 }

 export default CompleteTask